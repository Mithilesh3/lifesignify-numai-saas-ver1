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

export default function StepFinancial({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (
    field: keyof ReportFormData["financial"],
    value: string | number | undefined
  ) => {
    setFormData({
      ...formData,
      financial: {
        ...formData.financial,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Financial Snapshot</h2>

      <input
        type="number"
        placeholder="Monthly Income"
        className="input"
        value={formData.financial?.monthly_income || ""}
        onChange={(e) => update("monthly_income", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="0"
        max="100"
        placeholder="Savings Ratio (%)"
        className="input"
        value={formData.financial?.savings_ratio || ""}
        onChange={(e) => update("savings_ratio", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="0"
        max="100"
        placeholder="Debt Ratio (%)"
        className="input"
        value={formData.financial?.debt_ratio || ""}
        onChange={(e) => update("debt_ratio", toNumber(e.target.value))}
      />

      <select
        className="input"
        value={formData.financial?.risk_tolerance || ""}
        onChange={(e) => update("risk_tolerance", e.target.value || undefined)}
      >
        <option value="">Risk Tolerance</option>
        <option value="low">Low</option>
        <option value="moderate">Moderate</option>
        <option value="high">High</option>
      </select>

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
