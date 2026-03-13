import type { Dispatch, SetStateAction } from "react";
import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  setFormData: Dispatch<SetStateAction<ReportFormData>>;
  next: () => void;
  prev: () => void;
}

export default function StepBirthDetails({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (field: keyof ReportFormData["birth_details"], value: string) => {
    setFormData({
      ...formData,
      birth_details: {
        ...formData.birth_details,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Birth Details</h2>

      <input
        type="date"
        className="input"
        value={formData.birth_details?.date_of_birth || ""}
        onChange={(e) => update("date_of_birth", e.target.value)}
      />

      <input
        placeholder="Birth Place"
        className="input"
        value={formData.birth_details?.birthplace_city || ""}
        onChange={(e) => update("birthplace_city", e.target.value)}
      />

      <textarea
        placeholder="Current Problem / Main Concern"
        className="input min-h-28"
        value={formData.current_problem || ""}
        onChange={(e) =>
          setFormData({
            ...formData,
            current_problem: e.target.value,
          })
        }
      />

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">
          Back
        </button>
        <button
          onClick={next}
          className="btn-primary"
          disabled={
            !formData.birth_details?.date_of_birth ||
            !formData.birth_details?.birthplace_city ||
            !formData.current_problem?.trim()
          }
        >
          Continue
        </button>
      </div>
    </div>
  );
}
