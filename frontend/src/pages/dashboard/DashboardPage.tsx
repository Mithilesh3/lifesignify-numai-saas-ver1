import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import { useUsage } from "../../context/UsageContext";
import toast from "react-hot-toast";
import { motion } from "framer-motion";

interface Report {
  id: number;
  created_at: string;
  content: {
    executive_brief?: {
      summary?: string;
    };
    core_metrics?: {
      life_stability_index?: number;
      risk_band?: string;
      confidence_score?: number;
    };
  };
}

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const { usage } = useUsage();
  const navigate = useNavigate();

  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  const currentPlan =
    user?.subscription?.plan_name?.toLowerCase() ||
    user?.organization?.plan?.toLowerCase() ||
    "none";

  const isActive = user?.subscription?.is_active ?? false;

  const used = usage?.reports_used || 0;
  const limit = usage?.reports_limit || 0;
  const remaining = usage?.reports_remaining ?? Math.max(limit - used, 0);

  const usagePercent =
    limit > 0 ? Math.min((used / limit) * 100, 100) : 0;

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
    void fetchReports();
  }, []);

  const latestReport = reports[0];
  const latestMetrics = latestReport?.content?.core_metrics;
  const latestSummary = latestReport?.content?.executive_brief?.summary;

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-10">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Welcome back, {user?.email}</h1>
          <p className="text-gray-400 mt-1">
            Your Life Intelligence Executive Dashboard
          </p>
        </div>

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

      <div className="bg-gray-900 p-6 rounded-2xl shadow-lg">
        <div className="flex justify-between text-sm mb-2">
          <span>
            Reports Used: {used} / {limit}
          </span>
          <span>{remaining} remaining</span>
        </div>

        <div className="w-full bg-gray-800 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all ${
              usagePercent > 80
                ? "bg-red-500"
                : usagePercent > 50
                ? "bg-yellow-500"
                : "bg-emerald-500"
            }`}
            style={{ width: `${usagePercent}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <MetricCard label="Total Reports" value={loading ? "..." : reports.length} />
        <MetricCard
          label="Life Stability"
          value={latestMetrics?.life_stability_index ?? "--"}
        />
        <MetricCard label="Risk Band" value={latestMetrics?.risk_band ?? "--"} />
        <MetricCard
          label="Confidence Score"
          value={
            latestMetrics?.confidence_score !== undefined
              ? `${latestMetrics.confidence_score}%`
              : "--"
          }
        />
      </div>

      {latestSummary && (
        <div className="bg-gray-900 p-6 rounded-2xl shadow-lg">
          <h2 className="text-xl font-semibold mb-3">Latest Summary</h2>
          <p className="text-gray-300 leading-7">{latestSummary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.button
          whileHover={{ scale: 1.03 }}
          onClick={() => navigate("/generate-report")}
          disabled={!isActive || limit <= 0 || used >= limit}
          className="bg-indigo-600 hover:bg-indigo-500 p-6 rounded-xl font-semibold transition disabled:opacity-50"
        >
          {!isActive || limit <= 0
            ? "No Active Plan"
            : used >= limit
            ? "Limit Reached"
            : "Generate AI Report"}
        </motion.button>

        <Link
          to="/reports"
          className="bg-indigo-600 hover:bg-indigo-500 p-6 rounded-xl font-semibold text-center"
        >
          View All Reports
        </Link>

        {(!isActive || used >= limit) && (
          <Link
            to="/billing"
            className="bg-emerald-600 hover:bg-emerald-500 p-6 rounded-xl font-semibold text-center"
          >
            Upgrade Plan
          </Link>
        )}
      </div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string | number }) {
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
        plan === "premium"
          ? "bg-purple-600"
          : plan === "pro"
          ? "bg-emerald-600"
          : "bg-gray-700"
      }`}
    >
      {plan.toUpperCase()} PLAN
    </div>
  );
}
