export type LifeFocus =
  | "finance_debt"
  | "career_growth"
  | "relationship"
  | "health_stability"
  | "emotional_confusion"
  | "business_decision"
  | "general_alignment";

export type LanguagePreference = "hindi" | "hinglish" | "english";
export type CareerType = "business" | "job" | "";
export type RiskTolerance = "low" | "moderate" | "high" | "";

export interface ReportFormData {
  identity: {
    full_name?: string;
    gender?: "male" | "female" | "other" | "";
    country_of_residence?: string;
    email?: string;
    partner_name?: string;
    business_name?: string;
    signature_style?: string;
  };
  birth_details: {
    date_of_birth?: string;
    time_of_birth?: string;
    birthplace_city?: string;
    birthplace_country?: string;
  };
  focus: {
    life_focus?: LifeFocus | "";
  };
  contact: {
    mobile_number?: string;
    social_handle?: string;
    domain_handle?: string;
    residence_number?: string;
    vehicle_number?: string;
  };
  preferences: {
    language_preference?: LanguagePreference;
    profession?: string;
    relationship_status?: string;
    career_type?: CareerType;
    primary_goal?: string;
  };
  career: {
    industry?: string;
    years_experience?: number;
    stress_level?: number;
  };
  financial: {
    monthly_income?: number;
    savings_ratio?: number;
    debt_ratio?: number;
    risk_tolerance?: RiskTolerance;
  };
  emotional: {
    anxiety_level?: number;
    decision_confusion?: number;
    impulse_control?: number;
    emotional_stability?: number;
  };
  life_events: {
    positive_events_years?: number[];
    setback_events_years?: number[];
  };
  calibration: {
    stress_response?: "withdraw" | "impulsive" | "overthink" | "take_control" | "";
    money_decision_style?: "emotional" | "calculated" | "risky" | "avoidant" | "";
    biggest_weakness?: "discipline" | "patience" | "confidence" | "focus" | "";
    life_preference?: "stability" | "growth" | "recognition" | "freedom" | "";
    decision_style?: "fast" | "research" | "advice" | "emotional" | "";
  };
  current_problem: string;
}

export interface ReportContent {
  meta?: {
    plan_tier?: string;
    generated_at?: string;
    used_fallback_narrative?: boolean;
    section_count?: number;
  };
  report_blueprint?: {
    plan_tier?: string;
    section_count?: number;
    sections?: Array<{
      order: number;
      key: string;
      title: string;
    }>;
  };
  current_problem?: string;
  executive_brief?: {
    summary?: string;
    key_strength?: string;
    key_risk?: string;
    strategic_focus?: string;
  };
  core_metrics?: {
    life_stability_index?: number;
    financial_discipline_index?: number;
    emotional_regulation_index?: number;
    dharma_alignment_score?: number;
    karma_pressure_index?: number;
    confidence_score?: number;
    data_completeness_score?: number;
    risk_band?: string;
  };
  analysis_sections?: Record<string, string>;
  radar_chart_data?: Record<string, number>;
  metrics_spine?: {
    primary_strength?: string;
    primary_deficit?: string;
    structural_cause?: string;
    intervention_focus?: string;
    risk_band?: string;
  };
  section_payloads?: Record<
    string,
    {
      title?: string;
      purpose?: string;
      key_inputs?: string[];
      output_fields?: string[];
      interpretation_logic?: string;
      tone_guidance?: string;
      narrative?: string;
      cards?: Array<{ label: string; value: string }>;
      bullets?: string[];
    }
  >;
}

export interface ReportResponse {
  id: number;
  title?: string;
  created_at: string;
  content: ReportContent;
}
