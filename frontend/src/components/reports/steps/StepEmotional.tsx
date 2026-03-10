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

export default function StepEmotional({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (field: string, value: number | undefined) => {
    setFormData({
      ...formData,
      emotional: {
        ...formData.emotional,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Emotional State</h2>

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Anxiety Level (1-10)"
        className="input"
        value={formData.emotional?.anxiety_level || ""}
        onChange={(e) => update("anxiety_level", toNumber(e.target.value))}
      />

      <input
        type="number"
        min="1"
        max="10"
        placeholder="Decision Confusion (1-10)"
        className="input"
        value={formData.emotional?.decision_confusion || ""}
        onChange={(e) => update("decision_confusion", toNumber(e.target.value))}
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
