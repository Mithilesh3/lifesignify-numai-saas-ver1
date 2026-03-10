import type { Dispatch, SetStateAction } from "react";
import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  setFormData: Dispatch<SetStateAction<ReportFormData>>;
  next: () => void;
  prev: () => void;
}

export default function StepBusiness({ formData, setFormData, next, prev }: Props) {
  const updateIdentity = (
    field: keyof ReportFormData["identity"],
    value: string
  ) => {
    setFormData({
      ...formData,
      identity: {
        ...formData.identity,
        [field]: value,
      },
    });
  };

  const updateContact = (
    field: keyof ReportFormData["contact"],
    value: string
  ) => {
    setFormData({
      ...formData,
      contact: {
        ...formData.contact,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Business & Relationship Context</h2>

      <input
        placeholder="Business Name (optional)"
        className="input"
        value={formData.identity?.business_name || ""}
        onChange={(e) => updateIdentity("business_name", e.target.value)}
      />

      <input
        placeholder="Partner Name (optional)"
        className="input"
        value={formData.identity?.partner_name || ""}
        onChange={(e) => updateIdentity("partner_name", e.target.value)}
      />

      <input
        placeholder="Social Handle (optional)"
        className="input"
        value={formData.contact?.social_handle || ""}
        onChange={(e) => updateContact("social_handle", e.target.value)}
      />

      <input
        placeholder="Domain Handle (optional)"
        className="input"
        value={formData.contact?.domain_handle || ""}
        onChange={(e) => updateContact("domain_handle", e.target.value)}
      />

      <input
        placeholder="Residence / Flat Number (optional)"
        className="input"
        value={formData.contact?.residence_number || ""}
        onChange={(e) => updateContact("residence_number", e.target.value)}
      />

      <input
        placeholder="Vehicle Number (optional)"
        className="input"
        value={formData.contact?.vehicle_number || ""}
        onChange={(e) => updateContact("vehicle_number", e.target.value)}
      />

      <p className="text-sm text-gray-400">
        These fields feed business, brand handle, residence energy, and vehicle vibration intelligence.
      </p>

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
