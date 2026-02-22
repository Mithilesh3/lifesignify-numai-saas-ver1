import { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import API from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import toast from "react-hot-toast";
import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

/* ============================
   UPDATED INTERFACES
============================ */

interface RiskAnalysis {
  burnout_risk?: number;
  overall_risk_level?: string;
  karma_pressure_level?: string;
  financial_stress_probability?: number;
}

interface Report {
  id: number;
  created_at: string;
  content: {
    executive_dashboard?: {
      life_stability_index?: number;
    };
    risk_analysis?: RiskAnalysis;
  };
}

export default function DashboardPage() {
  const { user, logout } = useAuth(); // ✅ added logout
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  /* ============================
     PLAN LOGIC
  ============================ */

  const currentPlan = user?.organization?.plan?.toLowerCase() || "basic";

  const limit =
    currentPlan === "pro"
      ? 50
      : currentPlan === "enterprise"
      ? 999999
      : 10;

  const used = user?.subscription?.reports_used || 0;
  const remaining = Math.max(limit - used, 0);
  const usagePercent = Math.min((used / limit) * 100, 100);

  const fetchReports = async () => {
    try {
      const res = await API.get("/reports/");
      setReports(res.data);
    } catch {
      toast.error("Failed to fetch reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleGenerateReport = async () => {
    if (generating) return;

    if (remaining <= 0) {
      toast.error("Report limit reached. Please upgrade your plan.");
      return;
    }

    setGenerating(true);
    const loadingToast = toast.loading("Generating AI report...");

    try {
      await API.post("/reports/generate-ai-report", {
        identity: {
          full_name: user?.email || "Test User",
          date_of_birth: "01/01/1990",
          gender: "male",
          country_of_residence: "India",
        },
        birth_details: {
          date_of_birth: "01/01/1990",
          time_of_birth: "10:30 AM",
          birthplace_city: "Mumbai",
          birthplace_country: "India",
        },
        focus: {
          life_focus: "general_alignment",
        },
      });

      toast.success("Report generated successfully 🚀", {
        id: loadingToast,
      });

      await fetchReports();
    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail || "Report generation failed",
        { id: loadingToast }
      );
    } finally {
      setGenerating(false);
    }
  };

  const latestReport = reports[0];

  /* ============================
     CHART DATA
  ============================ */

  const chartData = useMemo(() => {
    return reports
      .slice()
      .reverse()
      .map((r, index) => ({
        name: `R${index + 1}`,
        stability:
          r.content?.executive_dashboard?.life_stability_index || 0,
      }));
  }, [reports]);

  const risk = latestReport?.content?.risk_analysis;

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-10">

      {/* HEADER */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">
            Welcome back, {user?.email}
          </h1>
          <p className="text-gray-400 mt-1">
            Your Life Intelligence Executive Dashboard
          </p>
        </div>

        {/* ✅ Plan + Logout */}
        <div className="flex items-center gap-4">
          <PlanBadge plan={currentPlan} />

          <button
            onClick={logout}
            className="bg-red-600 hover:bg-red-500 px-4 py-2 rounded-lg text-sm font-semibold transition"
          >
            Logout
          </button>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <MetricCard
          label="Total Reports"
          value={loading ? "..." : reports.length}
        />

        <MetricCard
          label="Latest Stability Score"
          value={
            latestReport?.content?.executive_dashboard?.life_stability_index ?? "--"
          }
        />

        <MetricCard
          label="Overall Risk Level"
          value={risk?.overall_risk_level ?? "--"}
        />

        <MetricCard
          label="Burnout Risk"
          value={
            risk?.burnout_risk !== undefined
              ? `${risk.burnout_risk}%`
              : "--"
          }
        />
      </div>

      {/* RISK BREAKDOWN */}
      {risk && (
        <div className="bg-gray-900 p-6 rounded-2xl shadow-xl">
          <h2 className="text-lg font-semibold mb-4">
            Risk Breakdown
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-gray-400">Burnout</p>
              <p className="text-xl font-bold">{risk.burnout_risk}%</p>
            </div>

            <div>
              <p className="text-gray-400">Karma Pressure</p>
              <p className="text-xl font-bold">
                {risk.karma_pressure_level}
              </p>
            </div>

            <div>
              <p className="text-gray-400">Financial Stress</p>
              <p className="text-xl font-bold">
                {risk.financial_stress_probability}%
              </p>
            </div>

            <div>
              <p className="text-gray-400">Overall Risk</p>
              <p className="text-xl font-bold">
                {risk.overall_risk_level}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* CHART */}
      {reports.length > 0 && (
        <div className="bg-gray-900 p-6 rounded-2xl shadow-xl">
          <h2 className="text-lg font-semibold mb-4">
            Stability Trend Analysis
          </h2>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="stability"
                stroke="#6366f1"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* ACTIONS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.button
          whileHover={{ scale: 1.03 }}
          onClick={handleGenerateReport}
          disabled={generating || remaining <= 0}
          className="bg-indigo-600 hover:bg-indigo-500 p-6 rounded-xl font-semibold transition disabled:opacity-50"
        >
          {remaining <= 0
            ? "Limit Reached"
            : generating
            ? "Generating..."
            : "Generate AI Report"}
        </motion.button>

        <Link
          to="/reports"
          className="bg-indigo-600 hover:bg-indigo-500 p-6 rounded-xl font-semibold text-center"
        >
          View All Reports
        </Link>

        {currentPlan !== "pro" && (
          <Link
            to="/upgrade"
            className="bg-emerald-600 hover:bg-emerald-500 p-6 rounded-xl font-semibold text-center"
          >
            Upgrade to Pro
          </Link>
        )}
      </div>
    </div>
  );
}

/* ============================
   COMPONENTS
============================ */

function MetricCard({ label, value }: { label: string; value: any }) {
  return (
    <motion.div
      whileHover={{ scale: 1.04 }}
      className="bg-gray-900 p-6 rounded-2xl shadow-lg"
    >
      <p className="text-sm text-gray-400">{label}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </motion.div>
  );
}

function PlanBadge({ plan }: { plan: string }) {
  return (
    <div
      className={`px-4 py-2 rounded-full text-sm font-semibold ${
        plan === "pro"
          ? "bg-emerald-600"
          : plan === "enterprise"
          ? "bg-purple-600"
          : "bg-gray-700"
      }`}
    >
      {plan.toUpperCase()} PLAN
    </div>
  );
}