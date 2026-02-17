import { useEffect, useState } from "react";
import API from "../../services/api";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";

export default function DashboardPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [latestReport, setLatestReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await API.get("/reports/");
      setReports(res.data);
      if (res.data.length > 0) {
        setLatestReport(res.data[res.data.length - 1]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const generateReport = async () => {
    try {
      setLoading(true);
      setError("");
      await API.post("/reports/generate-ai-report", {});
      await fetchReports();
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError("Upgrade to Pro to generate AI reports 🚀");
      } else {
        setError("Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async (reportId: number) => {
    const res = await API.get(`/reports/${reportId}/download`, {
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "LifeSignify_Report.pdf");
    document.body.appendChild(link);
    link.click();
  };

  const dashboard = latestReport?.content?.executive_dashboard;

  const radarData = dashboard
    ? [
        { subject: "Life", value: dashboard.life_stability_index },
        { subject: "Finance", value: dashboard.financial_discipline_index },
        { subject: "Dharma", value: dashboard.dharma_alignment_score },
        { subject: "Clarity", value: dashboard.decision_clarity_score },
        { subject: "Emotion", value: dashboard.emotional_regulation_index },
      ]
    : [];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-indigo-400">
          Intelligence Overview
        </h2>

        <button
          onClick={generateReport}
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-700 px-6 py-2 rounded-lg"
        >
          {loading ? "Generating..." : "Generate AI Report"}
        </button>
      </div>

      {error && (
        <div className="bg-red-900/40 text-red-400 p-4 rounded-lg">
          {error}
        </div>
      )}

      {!latestReport && (
        <div className="text-gray-400 text-lg">
          No reports yet. Generate your first AI report.
        </div>
      )}

      {latestReport && (
        <>
          {/* Cards */}
          <div className="grid grid-cols-3 gap-6">
            <Card title="Life Stability" value={dashboard?.life_stability_index} />
            <Card title="Financial Discipline" value={dashboard?.financial_discipline_index} />
            <Card title="Dharma Alignment" value={dashboard?.dharma_alignment_score} />
          </div>

          {/* Radar Chart */}
          <div className="bg-[#1e293b] p-6 rounded-xl">
            <RadarChart outerRadius={150} width={500} height={400} data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar
                name="Score"
                dataKey="value"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.6}
              />
            </RadarChart>
          </div>

          {/* Reports List */}
          <div className="bg-[#0f172a] p-6 rounded-xl">
            <h3 className="text-xl font-semibold mb-4 text-indigo-300">
              Previous Reports
            </h3>

            <div className="space-y-3">
              {reports.map((r) => (
                <div
                  key={r.id}
                  className="flex justify-between bg-[#1e293b] p-4 rounded-lg"
                >
                  <span>Report #{r.id}</span>
                  <button
                    onClick={() => downloadPDF(r.id)}
                    className="text-indigo-400 hover:underline"
                  >
                    Download PDF
                  </button>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function Card({ title, value }: any) {
  return (
    <div className="bg-[#1e293b] p-6 rounded-xl">
      <h3 className="text-sm text-gray-400">{title}</h3>
      <p className="text-3xl font-bold mt-2 text-emerald-400">
        {value ?? "--"}
      </p>
    </div>
  );
}
