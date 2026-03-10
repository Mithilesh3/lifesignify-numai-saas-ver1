interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
  prev: () => void;
}

export default function StepFocus({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (value: string) => {
    setFormData({
      ...formData,
      focus: { life_focus: value },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Primary Focus</h2>

      <select
        className="input"
        value={formData.focus?.life_focus || ""}
        onChange={(e) => update(e.target.value)}
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
