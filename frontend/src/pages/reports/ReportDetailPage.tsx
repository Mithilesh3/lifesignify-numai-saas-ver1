import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import RadarChartComponent from "../../components/dashboard/RadarChartComponent";
import { useAuth } from "../../context/AuthContext";
import API from "../../services/api";
import type { ReportResponse } from "../../types/report";

const ANALYSIS_LABELS: Record<string, string> = {
  career_analysis: "Career Analysis",
  decision_profile: "Decision Profile",
  emotional_analysis: "Emotional Analysis",
  financial_analysis: "Financial Analysis",
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
    } catch {
      toast.error("Failed to download PDF", { id: loadingToast });
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
  const confidenceScore = metrics?.confidence_score ?? 0;
  const showInputWarning = usedFallbackNarrative || confidenceScore <= 25;
  const analysisEntries = Object.entries(content.analysis_sections || {});
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
          This report was generated with limited scoring input, so some metrics
          may stay near the neutral baseline. For final manual testing, generate
          one report with full financial, emotional, work-stress, and life-event
          data.
        </div>
      )}

      {summary && (
        <div className="bg-gray-900 p-6 rounded-xl shadow-md space-y-4">
          <h2 className="text-xl font-semibold">Executive Brief</h2>
          {summary.summary && (
            <p className="text-gray-300 leading-7">{summary.summary}</p>
          )}
          {summary.key_strength && (
            <p>
              <span className="text-emerald-400 font-semibold">
                Key strength:
              </span>{" "}
              {summary.key_strength}
            </p>
          )}
          {summary.key_risk && (
            <p>
              <span className="text-yellow-400 font-semibold">Key risk:</span>{" "}
              {summary.key_risk}
            </p>
          )}
          {summary.strategic_focus && (
            <p>
              <span className="text-indigo-400 font-semibold">
                Strategic focus:
              </span>{" "}
              {summary.strategic_focus}
            </p>
          )}
        </div>
      )}

      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ScoreCard
            label="Life Stability"
            value={metrics.life_stability_index}
          />
          <ScoreCard
            label="Financial Discipline"
            value={metrics.financial_discipline_index}
          />
          <ScoreCard
            label="Emotional Regulation"
            value={metrics.emotional_regulation_index}
          />
          <ScoreCard
            label="Dharma Alignment"
            value={metrics.dharma_alignment_score}
          />
          <ScoreCard label="Confidence Score" value={metrics.confidence_score} />
          <ScoreCard label="Risk Band" value={metrics.risk_band || "--"} />
        </div>
      )}

      {radarData.length > 0 && <RadarChartComponent data={radarData} />}

      {analysisEntries.length > 0 && (
        <div className="bg-gray-900 p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-6">Analysis</h2>
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
