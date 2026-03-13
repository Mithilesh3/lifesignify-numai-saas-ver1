import type { Dispatch, SetStateAction } from "react";
import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  setFormData: Dispatch<SetStateAction<ReportFormData>>;
  next: () => void;
}

export default function StepIdentity({ formData, setFormData, next }: Props) {
  const updateIdentity = (field: keyof ReportFormData["identity"], value: string) => {
    setFormData({
      ...formData,
      identity: {
        ...formData.identity,
        [field]: value,
      },
    });
  };

  const updateContact = (mobile_number: string) => {
    setFormData({
      ...formData,
      contact: {
        ...formData.contact,
        mobile_number,
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
        onChange={(e) => updateIdentity("full_name", e.target.value)}
      />

      <input
        placeholder="Mobile Number"
        className="input"
        value={formData.contact?.mobile_number || ""}
        onChange={(e) => updateContact(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email Address"
        className="input"
        value={formData.identity?.email || ""}
        onChange={(e) => updateIdentity("email", e.target.value)}
      />

      <select
        className="input"
        value={formData.identity?.gender || ""}
        onChange={(e) => updateIdentity("gender", e.target.value)}
      >
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>

      <button
        onClick={next}
        className="btn-primary"
        disabled={
          !formData.identity?.full_name
          || !formData.contact?.mobile_number
          || !formData.identity?.gender
        }
      >
        Continue
      </button>
    </div>
  );
}
