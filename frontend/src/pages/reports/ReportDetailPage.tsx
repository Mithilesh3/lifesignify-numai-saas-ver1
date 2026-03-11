import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import RadarChartComponent from "../../components/dashboard/RadarChartComponent";
import { useAuth } from "../../context/AuthContext";
import API from "../../services/api";
import type { ReportResponse } from "../../types/report";

const ANALYSIS_LABELS: Record<string, string> = {
  career_analysis: "करियर विश्लेषण | Career Analysis",
  decision_profile: "निर्णय प्रोफाइल | Decision Profile",
  emotional_analysis: "भावनात्मक विश्लेषण | Emotional Analysis",
  financial_analysis: "वित्तीय विश्लेषण | Financial Analysis",
};

export default function ReportDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [report, setReport] = useState<ReportResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");

  const plan =
    user?.subscription?.plan_name?.toLowerCase() ||
    user?.organization?.plan?.toLowerCase() ||
    "basic";

  useEffect(() => {
    if (!id) {
      setLoading(false);
      setError("Report not found.");
      return;
    }

    const fetchReport = async () => {
      try {
        const res = await API.get(`/reports/${id}`);
        setReport(res.data);
      } catch (requestError: unknown) {
        const detail = axios.isAxiosError(requestError)
          ? requestError.response?.data?.detail
          : undefined;
        setError(
          detail || "Failed to load report."
        );
        toast.error("Failed to load report");
      } finally {
        setLoading(false);
      }
    };

    void fetchReport();
  }, [id]);

  const downloadPDF = async () => {
    if (!id) {
      return;
    }

    setDownloading(true);
    const loadingToast = toast.loading("Preparing PDF...");

    try {
      const endpoint =
        plan === "basic"
          ? `/reports/${id}/preview-pdf`
          : `/reports/${id}/export-pdf`;

      const response = await API.get(endpoint, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `report-${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast.success("Report downloaded successfully", { id: loadingToast });
    } catch (requestError: unknown) {
      let detail: string | undefined;
      if (axios.isAxiosError(requestError)) {
        const payload = requestError.response?.data;
        if (payload instanceof Blob) {
          try {
            const text = await payload.text();
            const parsed = JSON.parse(text);
            detail = parsed?.detail;
          } catch {
            detail = undefined;
          }
        } else {
          detail = payload?.detail;
        }
      }
      toast.error(detail || "Failed to download PDF", { id: loadingToast });
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="animate-pulse text-lg">Loading Report...</div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="min-h-screen bg-gray-950 text-red-400 flex items-center justify-center">
        {error || "Report not found."}
      </div>
    );
  }

  const content = report.content || {};
  const summary = content.executive_brief;
  const metrics = content.core_metrics;
  const reportPlan = content.meta?.plan_tier || plan;
  const usedFallbackNarrative = Boolean(content.meta?.used_fallback_narrative);
  const decisionClarityScore = metrics?.confidence_score ?? 0;
  const dataCompletenessScore =
    metrics?.data_completeness_score ?? metrics?.confidence_score ?? 0;
  const showInputWarning = usedFallbackNarrative || dataCompletenessScore <= 45;
  const analysisEntries = Object.entries(content.analysis_sections || {});
  const metricsSpine = content.metrics_spine;
  const blueprintSections = content.report_blueprint?.sections || [];
  const sectionOrder = new Map(
    blueprintSections.map((section) => [section.key, section.order])
  );
  const sectionPayloadEntries = Object.entries(content.section_payloads || {}).sort(
    ([keyA], [keyB]) => {
      const orderA = sectionOrder.get(keyA) ?? Number.MAX_SAFE_INTEGER;
      const orderB = sectionOrder.get(keyB) ?? Number.MAX_SAFE_INTEGER;
      return orderA - orderB;
    }
  );
  const radarData = Object.entries(content.radar_chart_data || {}).map(
    ([metric, score]) => ({ metric, score: Number(score) })
  );

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-10">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            {report.title || "Life Intelligence Report"}
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            Plan: {reportPlan.toUpperCase()} | Generated{" "}
            {new Date(report.created_at).toLocaleString()}
          </p>
        </div>

        <div className="flex gap-4">
          <button
            onClick={() => navigate("/generate-report")}
            className="bg-emerald-600 hover:bg-emerald-500 px-5 py-2 rounded-lg transition"
          >
            Create Another Report
          </button>

          <button
            onClick={downloadPDF}
            disabled={downloading}
            className="bg-indigo-600 hover:bg-indigo-500 transition px-5 py-2 rounded-lg disabled:opacity-50"
          >
            {downloading ? "Preparing PDF..." : "Download PDF"}
          </button>
        </div>
      </div>

      {showInputWarning && (
        <div className="rounded-xl border border-amber-500/40 bg-amber-500/10 p-5 text-amber-100">
          Input completeness {dataCompletenessScore}% है। कुछ behavioral inputs
          limited होने के कारण कुछ metrics neutral baseline के करीब रह सकते हैं।
          Final validation के लिए एक report full financial, emotional, stress,
          और life-event intake के साथ generate करें।
        </div>
      )}

      {(content.report_blueprint?.section_count || content.meta?.section_count) && (
        <div className="rounded-xl border border-sky-500/30 bg-sky-500/10 p-5 text-sky-100">
          Blueprint coverage:{" "}
          {content.report_blueprint?.section_count || content.meta?.section_count}{" "}
          structured sections aligned to the {reportPlan.toUpperCase()} backend tier.
        </div>
      )}

      {summary && (
        <div className="bg-gray-900 p-6 rounded-xl shadow-md space-y-4">
          <h2 className="text-xl font-semibold">एग्जीक्यूटिव ब्रीफ | Executive Brief</h2>
          {summary.summary && (
            <p className="text-gray-300 leading-7">{summary.summary}</p>
          )}
          {summary.key_strength && (
            <p>
              <span className="text-emerald-400 font-semibold">
                मुख्य ताकत | Key strength:
              </span>{" "}
              {summary.key_strength}
            </p>
          )}
          {summary.key_risk && (
            <p>
              <span className="text-yellow-400 font-semibold">मुख्य जोखिम | Key risk:</span>{" "}
              {summary.key_risk}
            </p>
          )}
          {summary.strategic_focus && (
            <p>
                <span className="text-indigo-400 font-semibold">
                  रणनीतिक फोकस | Strategic focus:
                </span>{" "}
                {summary.strategic_focus}
            </p>
          )}
        </div>
      )}

      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ScoreCard
            label="जीवन स्थिरता | Life Stability"
            value={metrics.life_stability_index}
          />
          <ScoreCard
            label="वित्त अनुशासन | Financial Discipline"
            value={metrics.financial_discipline_index}
          />
          <ScoreCard
            label="भावनात्मक संतुलन | Emotional Regulation"
            value={metrics.emotional_regulation_index}
          />
          <ScoreCard
            label="धर्म संरेखण | Dharma Alignment"
            value={metrics.dharma_alignment_score}
          />
          <ScoreCard label="निर्णय स्पष्टता | Decision Clarity" value={decisionClarityScore} />
          <ScoreCard label="इनपुट पूर्णता | Input Completeness" value={dataCompletenessScore} />
          <ScoreCard label="रिस्क बैंड | Risk Band" value={metrics.risk_band || "--"} />
        </div>
      )}

      {metricsSpine && (
        <div className="bg-gray-900 p-6 rounded-xl shadow-md space-y-3">
          <h2 className="text-xl font-semibold">मेट्रिक्स डायग्नोस्टिक स्पाइन | Metrics Diagnostic Spine</h2>
          <p>
              <span className="text-emerald-400 font-semibold">
                मुख्य ताकत | Primary strength:
              </span>{" "}
              {metricsSpine.primary_strength || "--"}
          </p>
          <p>
              <span className="text-yellow-400 font-semibold">
                मुख्य कमी | Primary deficit:
              </span>{" "}
              {metricsSpine.primary_deficit || "--"}
          </p>
          <p>
              <span className="text-sky-400 font-semibold">
                संरचनात्मक कारण | Structural cause:
              </span>{" "}
              {metricsSpine.structural_cause || "--"}
          </p>
          <p>
              <span className="text-indigo-400 font-semibold">
                इंटरवेंशन फोकस | Intervention focus:
              </span>{" "}
              {metricsSpine.intervention_focus || "--"}
          </p>
          <p>
            <span className="text-rose-400 font-semibold">रिस्क बैंड | Risk band:</span>{" "}
            {metricsSpine.risk_band || "--"}
          </p>
        </div>
      )}

      {radarData.length > 0 && <RadarChartComponent data={radarData} />}

      {analysisEntries.length > 0 && (
        <div className="bg-gray-900 p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-6">विश्लेषण | Analysis</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {analysisEntries.map(([label, value]) => (
              <div key={label} className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-sm uppercase tracking-wide text-gray-400 mb-2">
                  {ANALYSIS_LABELS[label] || label.replace(/_/g, " ")}
                </h3>
                <p className="text-gray-200 leading-7">{value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {sectionPayloadEntries.length > 0 && reportPlan !== "basic" && (
        <div className="bg-gray-900 p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-6">
            रणनीतिक इंटेलिजेंस लेयर्स | Strategic Intelligence Layers
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {sectionPayloadEntries.map(([key, section]) => (
              <div key={key} className="bg-gray-800 p-4 rounded-lg space-y-3">
                <h3 className="text-sm uppercase tracking-wide text-indigo-300">
                  {section.title || key.replace(/_/g, " ")}
                </h3>
                {section.narrative && (
                  <p className="text-gray-200 leading-7">{section.narrative}</p>
                )}
                {(section.cards || []).slice(0, 4).map((card, index) => (
                  <p key={`${key}-${index}`} className="text-sm text-gray-300">
                    <span className="font-semibold text-gray-100">
                      {card.label}:
                    </span>{" "}
                    {card.value}
                  </p>
                ))}
                {(section.bullets || []).length > 0 && (
                  <ul className="list-disc pl-5 text-sm text-gray-300 space-y-1">
                    {section.bullets!.slice(0, 4).map((bullet, index) => (
                      <li key={`${key}-bullet-${index}`}>{bullet}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreCard({
  label,
  value,
}: {
  label: string;
  value?: number | string;
}) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-md">
      <p className="text-sm text-gray-400">{label}</p>
      <p className="text-3xl font-bold mt-2">{value ?? "--"}</p>
    </div>
  );
}
