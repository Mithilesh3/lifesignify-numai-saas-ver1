interface Props {
  formData: any;
  setFormData: any;
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
  const update = (field: string, value: string | number | undefined) => {
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
