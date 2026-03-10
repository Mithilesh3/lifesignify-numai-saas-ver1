import type { Dispatch, SetStateAction } from "react";
import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  setFormData: Dispatch<SetStateAction<ReportFormData>>;
  next: () => void;
  prev: () => void;
}

export default function StepFocus({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const updateFocus = (value: ReportFormData["focus"]["life_focus"]) => {
    setFormData({
      ...formData,
      focus: { life_focus: value },
    });
  };

  const updatePreferences = (
    field: keyof ReportFormData["preferences"],
    value: string
  ) => {
    setFormData({
      ...formData,
      preferences: {
        ...formData.preferences,
        [field]: value,
      },
      career:
        field === "profession"
          ? {
              ...formData.career,
              industry: value,
            }
          : formData.career,
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Primary Focus</h2>

      <select
        className="input"
        value={formData.focus?.life_focus || ""}
        onChange={(e) =>
          updateFocus(e.target.value as ReportFormData["focus"]["life_focus"])
        }
      >
        <option value="">Select</option>
        <option value="career_growth">Career Growth</option>
        <option value="finance_debt">Finance and Debt</option>
        <option value="relationship">Relationship</option>
        <option value="health_stability">Health Stability</option>
        <option value="emotional_confusion">Emotional Confusion</option>
        <option value="business_decision">Business Decision</option>
        <option value="general_alignment">General Alignment</option>
      </select>

      <textarea
        placeholder="Current problem or main reason for generating this report"
        className="input min-h-28"
        value={formData.current_problem || ""}
        onChange={(e) =>
          setFormData({
            ...formData,
            current_problem: e.target.value,
          })
        }
      />

      <input
        placeholder="Primary Goal"
        className="input"
        value={formData.preferences?.primary_goal || ""}
        onChange={(e) => updatePreferences("primary_goal", e.target.value)}
      />

      <input
        placeholder="Profession / Industry"
        className="input"
        value={formData.preferences?.profession || ""}
        onChange={(e) => updatePreferences("profession", e.target.value)}
      />

      <select
        className="input"
        value={formData.preferences?.career_type || ""}
        onChange={(e) => updatePreferences("career_type", e.target.value)}
      >
        <option value="">Career Type</option>
        <option value="job">Job</option>
        <option value="business">Business</option>
      </select>

      <input
        placeholder="Relationship Status"
        className="input"
        value={formData.preferences?.relationship_status || ""}
        onChange={(e) => updatePreferences("relationship_status", e.target.value)}
      />

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">
          Back
        </button>
        <button onClick={next} className="btn-primary" disabled={!formData.focus?.life_focus}>
          Continue
        </button>
      </div>
    </div>
  );
}
