import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  submit: () => void;
  prev: () => void;
  submitting?: boolean;
}

export default function StepReview({ formData, submit, prev, submitting }: Props) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold mb-6">Review & Generate</h2>

      <div className="bg-gray-900 rounded-xl p-5 space-y-3 text-sm text-gray-300">
        <p>
          <span className="text-gray-400">Name:</span> {formData.identity?.full_name || "--"}
        </p>
        <p>
          <span className="text-gray-400">Mobile:</span>{" "}
          {formData.contact?.mobile_number || "--"}
        </p>
        <p>
          <span className="text-gray-400">Email:</span> {formData.identity?.email || "--"}
        </p>
        <p>
          <span className="text-gray-400">Date of Birth:</span>{" "}
          {formData.birth_details?.date_of_birth || "--"}
        </p>
        <p>
          <span className="text-gray-400">Birth Place:</span>{" "}
          {formData.birth_details?.birthplace_city || "--"}
        </p>
        <p>
          <span className="text-gray-400">Gender:</span> {formData.identity?.gender || "--"}
        </p>
        <p>
          <span className="text-gray-400">Current Problem:</span>{" "}
          {formData.current_problem || "--"}
        </p>
      </div>

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">
          Back
        </button>

        <button
          onClick={submit}
          disabled={submitting}
          className="bg-green-600 hover:bg-green-500 px-6 py-2 rounded-lg"
        >
          {submitting ? "Generating..." : "Generate Report"}
        </button>
      </div>
    </div>
  );
}
