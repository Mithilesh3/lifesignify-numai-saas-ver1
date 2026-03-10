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

  const updatePreference = (
    field: keyof ReportFormData["preferences"],
    value: string
  ) => {
    setFormData({
      ...formData,
      preferences: {
        ...formData.preferences,
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
        onChange={(e) => updateIdentity("full_name", e.target.value)}
      />

      <input
        type="email"
        placeholder="Email Address"
        className="input"
        value={formData.identity?.email || ""}
        onChange={(e) => updateIdentity("email", e.target.value)}
      />

      <input
        placeholder="Signature Style (optional)"
        className="input"
        value={formData.identity?.signature_style || ""}
        onChange={(e) => updateIdentity("signature_style", e.target.value)}
      />

      <input
        placeholder="Mobile Number"
        className="input"
        value={formData.contact?.mobile_number || ""}
        onChange={(e) => updateContact(e.target.value)}
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

      <input
        placeholder="Country of Residence"
        className="input"
        value={formData.identity?.country_of_residence || ""}
        onChange={(e) => updateIdentity("country_of_residence", e.target.value)}
      />

      <select
        className="input"
        value={formData.preferences?.language_preference || "hindi"}
        onChange={(e) => updatePreference("language_preference", e.target.value)}
      >
        <option value="hindi">Hindi</option>
        <option value="hinglish">Hinglish</option>
        <option value="english">English</option>
      </select>

      <p className="text-sm text-gray-400">
        Mobile, signature style, and language now feed correction-led personalization in the report engine.
      </p>

      <button
        onClick={next}
        className="btn-primary"
        disabled={!formData.identity?.full_name || !formData.identity?.country_of_residence}
      >
        Continue
      </button>
    </div>
  );
}
