interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
}

export default function StepIdentity({ formData, setFormData, next }: Props) {
  const update = (field: string, value: string) => {
    setFormData({
      ...formData,
      identity: {
        ...formData.identity,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Identity Details</h2>

      <input
        placeholder="Full Name"
        className="input"
        value={formData.identity?.full_name || ""}
        onChange={(e) => update("full_name", e.target.value)}
      />

      <select
        className="input"
        value={formData.identity?.gender || ""}
        onChange={(e) => update("gender", e.target.value)}
      >
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>

      <input
        placeholder="Country of Residence"
        className="input"
        value={formData.identity?.country_of_residence || ""}
        onChange={(e) => update("country_of_residence", e.target.value)}
      />

      <button onClick={next} className="btn-primary">
        Continue
      </button>
    </div>
  );
}
