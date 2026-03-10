import type { Dispatch, SetStateAction } from "react";
import type { ReportFormData } from "../../../types/report";

interface Props {
  formData: ReportFormData;
  setFormData: Dispatch<SetStateAction<ReportFormData>>;
  next: () => void;
  prev: () => void;
}

const parseYears = (value: string): number[] | undefined => {
  const years = value
    .split(",")
    .map((item) => Number(item.trim()))
    .filter((year) => Number.isInteger(year) && year > 1900 && year < 2100);

  return years.length > 0 ? years : undefined;
};

const formatYears = (years?: number[]) => (years && years.length ? years.join(", ") : "");

export default function StepHealth({ formData, setFormData, next, prev }: Props) {
  const updateLifeEvents = (
    field: keyof ReportFormData["life_events"],
    value: string
  ) => {
    setFormData({
      ...formData,
      life_events: {
        ...formData.life_events,
        [field]: parseYears(value),
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Life Events Snapshot</h2>

      <input
        placeholder="Positive milestone years (comma separated, e.g. 2017, 2023)"
        className="input"
        value={formatYears(formData.life_events?.positive_events_years)}
        onChange={(e) => updateLifeEvents("positive_events_years", e.target.value)}
      />

      <input
        placeholder="Setback years (comma separated, e.g. 2020, 2022)"
        className="input"
        value={formatYears(formData.life_events?.setback_events_years)}
        onChange={(e) => updateLifeEvents("setback_events_years", e.target.value)}
      />

      <p className="text-sm text-gray-400">
        Setback years directly affect the backend stability and pressure scoring.
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
