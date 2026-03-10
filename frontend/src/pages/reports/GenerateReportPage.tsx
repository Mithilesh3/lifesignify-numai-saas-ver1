import { useState } from "react";
import type { ComponentType, Dispatch, SetStateAction } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import API from "../../services/api";
import { useAuth } from "../../context/AuthContext";

import StepIdentity from "../../components/reports/steps/StepIdentity";
import StepBirthDetails from "../../components/reports/steps/StepBirthDetails";
import StepFocus from "../../components/reports/steps/StepFocus";
import StepFinancial from "../../components/reports/steps/StepFinancial";
import StepEmotional from "../../components/reports/steps/StepEmotional";
import StepBusiness from "../../components/reports/steps/StepBusiness";
import StepHealth from "../../components/reports/steps/StepHealth";
import StepCalibration from "../../components/reports/steps/StepCalibration";
import StepReview from "../../components/reports/steps/StepReview";
import type { ReportFormData } from "../../types/report";

type StepComponent = unknown;

interface ValidationErrorItem {
  loc?: Array<string | number>;
  msg?: string;
}

const hasValues = (value: Record<string, unknown> | undefined) =>
  Boolean(value) && Object.values(value as Record<string, unknown>).some(Boolean);

export default function GenerateReportPage() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState<ReportFormData>({
    identity: {},
    birth_details: {},
    focus: {},
    contact: {},
    preferences: {
      language_preference: "hindi",
    },
    career: {},
    financial: {},
    emotional: {},
    life_events: {},
    calibration: {},
    current_problem: "",
  });

  const plan = user?.subscription?.plan_name?.toLowerCase() || "basic";

  const steps: Array<{ key: string; component: StepComponent }> = [
    { key: "identity", component: StepIdentity },
    { key: "birth_details", component: StepBirthDetails },
    { key: "focus", component: StepFocus },
  ];

  if (plan !== "basic") {
    steps.push(
      { key: "financial", component: StepFinancial },
      { key: "emotional", component: StepEmotional }
    );
  }

  if (plan === "enterprise") {
    steps.push(
      { key: "business_context", component: StepBusiness },
      { key: "life_events", component: StepHealth },
      { key: "calibration", component: StepCalibration }
    );
  }

  steps.push({ key: "review", component: StepReview });

  const totalSteps = steps.length;
  const CurrentStepComponent = steps[step - 1]
    .component as ComponentType<{
    formData: ReportFormData;
    setFormData: Dispatch<SetStateAction<ReportFormData>>;
    next: () => void;
    prev: () => void;
    submit: () => void;
    plan: string;
    submitting: boolean;
  }>;

  const next = () => step < totalSteps && setStep(step + 1);
  const prev = () => step > 1 && setStep(step - 1);

  const handleSubmit = async () => {
    if (
      !formData.identity?.full_name ||
      !formData.identity?.country_of_residence ||
      !formData.birth_details?.date_of_birth ||
      !formData.birth_details?.birthplace_city ||
      !formData.birth_details?.birthplace_country ||
      !formData.focus?.life_focus
    ) {
      toast.error("Please fill all required fields.");
      return;
    }

    setSubmitting(true);

    try {
      const payload = {
        identity: {
          ...formData.identity,
          date_of_birth: formData.birth_details.date_of_birth,
        },
        birth_details: formData.birth_details,
        focus: formData.focus,
        current_problem: formData.current_problem?.trim() || undefined,
        contact: hasValues(formData.contact) ? formData.contact : undefined,
        preferences: hasValues(formData.preferences)
          ? formData.preferences
          : undefined,
        career: hasValues(formData.career) ? formData.career : undefined,
        financial: hasValues(formData.financial) ? formData.financial : undefined,
        emotional: hasValues(formData.emotional) ? formData.emotional : undefined,
        life_events: hasValues(formData.life_events)
          ? formData.life_events
          : undefined,
        calibration: hasValues(formData.calibration)
          ? formData.calibration
          : undefined,
      };

      const { data } = await API.post("/reports/generate-ai-report", payload);
      await refreshUser();

      toast.success("Report generated successfully");
      navigate(`/reports/${data.id}`);
    } catch (error: unknown) {
      if (axios.isAxiosError(error) && error.response?.status === 422) {
        const details = error.response.data?.detail;

        if (Array.isArray(details)) {
          const message = details
            .map(
              (err: ValidationErrorItem) => `${err.loc?.join(" -> ")} : ${err.msg}`
            )
            .join("\n");

          toast.error(message);
        } else {
          toast.error("Invalid input data.");
        }
      } else if (axios.isAxiosError(error) && error.response?.status === 403) {
        toast.error(
          error.response?.data?.detail ||
            "Your subscription does not allow this."
        );
      } else {
        toast.error("Something went wrong.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <div className="w-full bg-gray-800 h-2 rounded-full mb-6">
        <div
          className="bg-indigo-600 h-2 rounded-full transition-all"
          style={{ width: `${(step / totalSteps) * 100}%` }}
        />
      </div>

      <p className="text-sm text-gray-400 mb-6">
        Step {step} of {totalSteps}
      </p>

      <CurrentStepComponent
        formData={formData}
        setFormData={setFormData}
        next={next}
        prev={prev}
        submit={handleSubmit}
        plan={plan}
        submitting={submitting}
      />
    </div>
  );
}
