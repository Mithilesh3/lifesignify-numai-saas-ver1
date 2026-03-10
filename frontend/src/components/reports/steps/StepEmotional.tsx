import type { Dispatch, SetStateAction } from "react";
import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  setFormData: Dispatch<SetStateAction<ReportFormData>>;
  next: () => void;
  prev: () => void;
}

const toNumber = (value: string) => {
  if (!value) {
    return undefined;
  }

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : undefined;
};

export default function StepEmotional({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const updateEmotional = (
    field: keyof ReportFormData["emotional"],
    value: number | undefined
  ) => {
    setFormData({
      ...formData,
      emotional: {
        ...formData.emotional,
        [field]: value,
      },
    });
  };

  const updateCareer = (
    field: keyof ReportFormData["career"],
    value: number | undefined
  ) => {
    setFormData({
      ...formData,
      career: {
        ...formData.career,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Emotional & Career Signals</h2>

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Anxiety Level (1-10)"
        className="input"
        value={formData.emotional?.anxiety_level || ""}
        onChange={(e) => updateEmotional("anxiety_level", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Decision Confusion (1-10)"
        className="input"
        value={formData.emotional?.decision_confusion || ""}
        onChange={(e) => updateEmotional("decision_confusion", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Impulse Control (1-10)"
        className="input"
        value={formData.emotional?.impulse_control || ""}
        onChange={(e) => updateEmotional("impulse_control", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Emotional Stability (1-10)"
        className="input"
        value={formData.emotional?.emotional_stability || ""}
        onChange={(e) =>
          updateEmotional("emotional_stability", toNumber(e.target.value))
        }
      />

      <input
        type="number"
        min="0"
        placeholder="Years of Experience"
        className="input"
        value={formData.career?.years_experience || ""}
        onChange={(e) => updateCareer("years_experience", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Work Stress Level (1-10)"
        className="input"
        value={formData.career?.stress_level || ""}
        onChange={(e) => updateCareer("stress_level", toNumber(e.target.value))}
      />

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">
          Back
        </button>
        <button onClick={next} className="btn-primary">
          Continue
        </button>
      </div>
    </div>
  );
}
