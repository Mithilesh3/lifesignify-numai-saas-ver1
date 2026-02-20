// src/pages/dashboard/DashboardPage.tsx

import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import API from "../../services/api"

export default function DashboardPage() {
  const navigate = useNavigate()

  const [loading, setLoading] = useState(false)
  const [reports, setReports] = useState<any[]>([])

  const [formData, setFormData] = useState({
    full_name: "",
    date_of_birth: "",
    gender: "male",
    country_of_residence: "",
    time_of_birth: "",
    birthplace_city: "",
    birthplace_country: "",
    life_focus: "general_alignment"
  })

  // =========================
  // Fetch Reports
  // =========================
  const fetchReports = async () => {
    try {
      const res = await API.get("/reports/")
      setReports(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchReports()
  }, [])

  // =========================
  // Generate AI Report
  // =========================
  const generateReport = async () => {
    try {
      setLoading(true)

      const payload = {
        identity: {
          full_name: formData.full_name,
          date_of_birth: formData.date_of_birth,
          gender: formData.gender,
          country_of_residence: formData.country_of_residence
        },
        birth_details: {
          date_of_birth: formData.date_of_birth,
          time_of_birth: formData.time_of_birth,
          birthplace_city: formData.birthplace_city,
          birthplace_country: formData.birthplace_country
        },
        focus: {
          life_focus: formData.life_focus
        }
      }

      await API.post("/reports/generate-ai-report", payload)

      await fetchReports()
      alert("Report Generated Successfully 🚀")

    } catch (error: any) {
      if (error.response?.status === 403) {
        navigate("/upgrade")
      } else {
        console.error(error.response?.data)
        alert("Failed to generate report")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">

      <h1 className="text-3xl font-bold mb-6">
        LifeSignify Dashboard
      </h1>

      {/* Intake Form */}
      <div className="bg-gray-900 p-6 rounded-xl space-y-4 mb-10">

        <input
          placeholder="Full Name"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
        />

        <input
          type="date"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
        />

        <input
          placeholder="Country of Residence"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={(e) => setFormData({ ...formData, country_of_residence: e.target.value })}
        />

        <input
          placeholder="Birth City"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={(e) => setFormData({ ...formData, birthplace_city: e.target.value })}
        />

        <input
          placeholder="Birth Country"
          className="w-full p-3 bg-gray-800 rounded"
          onChange={(e) => setFormData({ ...formData, birthplace_country: e.target.value })}
        />

        <select
          className="w-full p-3 bg-gray-800 rounded"
          onChange={(e) => setFormData({ ...formData, life_focus: e.target.value })}
        >
          <option value="general_alignment">General Alignment</option>
          <option value="finance_debt">Finance & Debt</option>
          <option value="career_growth">Career Growth</option>
          <option value="relationship">Relationship</option>
          <option value="health_stability">Health Stability</option>
          <option value="business_decision">Business Decision</option>
        </select>

        <button
          onClick={generateReport}
          disabled={loading}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-3 rounded-xl w-full"
        >
          {loading ? "Generating..." : "Generate AI Report"}
        </button>

      </div>

      {/* Reports List */}
      <div>
        <h2 className="text-xl mb-4">Your Reports</h2>

        {reports.length === 0 ? (
          <p className="text-gray-400">No reports yet</p>
        ) : (
          <div className="space-y-3">
            {reports.map((report) => (
              <div
                key={report.id}
                className="bg-gray-800 p-4 rounded"
              >
                <h3 className="font-semibold">{report.title}</h3>
                <p className="text-gray-400 text-sm">
                  Created at: {new Date(report.created_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  )
}