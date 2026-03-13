import { useState } from "react";
import type { ComponentType, Dispatch, SetStateAction } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import API from "../../services/api";
import { useAuth } from "../../context/AuthContext";

import StepIdentity from "../../components/reports/steps/StepIdentity";
import StepBirthDetails from "../../components/reports/steps/StepBirthDetails";
import StepReview from "../../components/reports/steps/StepReview";
import type { ReportFormData } from "../../types/report";

type StepComponent = unknown;

interface ValidationErrorItem {
  loc?: Array<string | number>;
  msg?: string;
}

const hasValues = (value: Record<string, unknown> | undefined) => Boolean(value)
  && Object.values(value as Record<string, unknown>).some(Boolean);

const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

export default function GenerateReportPage() {
  const { refreshUser } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState<ReportFormData>({
    identity: {},
    birth_details: {},
    focus: { life_focus: "general_alignment" },
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

  const steps: Array<{ key: string; component: StepComponent }> = [
    { key: "identity", component: StepIdentity },
    { key: "birth_details", component: StepBirthDetails },
    { key: "review", component: StepReview },
  ];

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
    const fullName = formData.identity?.full_name?.trim();
    const mobileNumber = formData.contact?.mobile_number?.trim();
    const emailAddress = formData.identity?.email?.trim();
    const dateOfBirth = formData.birth_details?.date_of_birth;
    const birthPlace = formData.birth_details?.birthplace_city?.trim();
    const gender = formData.identity?.gender;
    const currentProblem = formData.current_problem?.trim();

    if (
      !fullName ||
      !mobileNumber ||
      !dateOfBirth ||
      !birthPlace ||
      !gender ||
      !currentProblem
    ) {
      toast.error("Please fill all required fields.");
      return;
    }

    if (emailAddress && !isValidEmail(emailAddress)) {
      toast.error("Please enter a valid email address.");
      return;
    }

    setSubmitting(true);

    try {
      const fallbackCountry = formData.identity?.country_of_residence?.trim() || "Not Specified";

      const payload = {
        identity: {
          ...formData.identity,
          full_name: fullName,
          email: emailAddress || undefined,
          gender,
          country_of_residence: fallbackCountry,
          date_of_birth: dateOfBirth,
        },
        birth_details: {
          ...formData.birth_details,
          date_of_birth: dateOfBirth,
          birthplace_city: birthPlace,
          birthplace_country:
            formData.birth_details?.birthplace_country?.trim() || fallbackCountry,
        },
        focus: {
          life_focus: formData.focus?.life_focus || "general_alignment",
        },
        current_problem: currentProblem,
        contact: hasValues({
          mobile_number: mobileNumber,
        })
          ? {
              mobile_number: mobileNumber,
            }
          : undefined,
        preferences: hasValues(formData.preferences)
          ? {
              ...formData.preferences,
              language_preference:
                formData.preferences?.language_preference || "hindi",
              primary_goal:
                formData.preferences?.primary_goal?.trim() || currentProblem,
            }
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
    <div className="max-w-2xl mx-auto py-10 px-4">
      <div className="w-full bg-gray-800 h-2 rounded-full mb-6">
        <div
          className="bg-indigo-600 h-2 rounded-full transition-all"
          style={{ width: `${(step / totalSteps) * 100}%` }}
        />
      </div>

      <p className="text-sm text-gray-400 mb-6">
        Step {step} of {totalSteps}
      </p>

      <div className="card border border-gray-800">
        <CurrentStepComponent
          formData={formData}
          setFormData={setFormData}
          next={next}
          prev={prev}
          submit={handleSubmit}
          plan="basic"
          submitting={submitting}
        />
      </div>
    </div>
  );
}
