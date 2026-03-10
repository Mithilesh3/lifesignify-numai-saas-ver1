from pathlib import Path
from io import BytesIO
import re
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

if "openai" not in sys.modules:
    openai_stub = types.ModuleType("openai")

    class _DummyAzureOpenAI:
        def __init__(self, *args, **kwargs):
            self.chat = types.SimpleNamespace(
                completions=types.SimpleNamespace(create=self._create),
            )

        def _create(self, *args, **kwargs):
            raise RuntimeError("Azure OpenAI client should not be called in the smoke test.")

    openai_stub.AzureOpenAI = _DummyAzureOpenAI
    sys.modules["openai"] = openai_stub

import app.modules.reports.ai_engine as report_ai_engine
from app.modules.reports.ai_engine import generate_life_signify_report
from app.modules.reports.intake_schema import LifeSignifyRequest
from app.modules.reports.pdf_engine import generate_report_pdf
from app.modules.reports.pdf_engine.fonts import register_fonts
from pypdf import PdfReader
from pypdf.generic import ContentStream

SAMPLE_REQUEST = {
    "full_name": "Rahul Sharma",
    "date_of_birth": "15-08-1993",
    "mobile_number": "9876543210",
    "gender": "male",
    "city": "Delhi",
    "country": "India",
    "email": "rahul.sharma@example.com",
    "language_preference": "hindi",
    "profession": "Technology",
    "career_type": "job",
    "relationship_status": "married",
    "primary_goal": "career growth and financial stability",
    "current_problem": "काम में growth रुक-रुक कर हो रही है और financial planning consistent नहीं है।",
    "financial": {
        "monthly_income": 95000,
        "savings_ratio": 22,
        "debt_ratio": 18,
        "risk_tolerance": "moderate",
    },
    "career": {
        "industry": "Technology",
        "years_experience": 8,
        "stress_level": 6,
    },
    "emotional": {
        "anxiety_level": 4,
        "decision_confusion": 5,
        "impulse_control": 7,
        "emotional_stability": 6,
    },
    "life_events": {
        "positive_events_years": [2017, 2023],
        "setback_events_years": [2020],
    },
}


def _stub_ai_narrative(*_args, **_kwargs):
    return {
        "executive_brief": {
            "summary": "राहुल शर्मा की Life Path energy बदलाव, learning और self-driven progress की तरफ मजबूत संकेत देती है। अभी career growth और financial discipline को एक साथ align करना सबसे महत्वपूर्ण theme है।",
            "key_strength": "आपकी सबसे बड़ी strength adaptability, fast learning और practical execution का blend है।",
            "key_risk": "जब stress बढ़ता है तब decision clarity थोड़ी slow हो सकती है, इसलिए structure जरूरी है।",
            "strategic_focus": "अगले 90 दिनों में career positioning, savings discipline और decision routine को same framework में लाना चाहिए।",
        },
        "analysis_sections": {
            "career_analysis": "Technology domain में आपकी progress तब तेज होती है जब role में ownership, visibility और growth track साफ हो। Repetitive work आपकी energy को नीचे खींच सकता है।",
            "decision_profile": "आप decisions intuition और logic के mix से लेते हैं, लेकिन high-pressure phases में written filters मदद करेंगे।",
            "emotional_analysis": "आपकी emotional regulation ठीक है, पर recovery routine maintain न हो तो focus जल्दी टूट सकता है।",
            "financial_analysis": "Income potential अच्छा है, लेकिन wealth creation के लिए disciplined savings और planned investing की जरूरत है।",
        },
        "primary_insight": {
            "narrative": "राहुल के लिए मुख्य रणनीतिक संकेत यह है कि growth को chance पर नहीं बल्कि structure पर चलाना होगा। Life Path change-friendly है, लेकिन financial और emotional rhythm को मजबूत किए बिना momentum टिकाऊ नहीं होगा।",
        },
        "archetype_intelligence": {
            "signature": "यह profile analysis और adaptability का blend दिखाती है, इसलिए shallow execution की बजाय thoughtful action ज्यादा suited रहेगा।",
            "shadow_traits": "Pressure phase में overthinking और scattered follow-through risk बन सकते हैं।",
            "growth_path": "Repeatable systems, visible weekly review और structured communication इस archetype का best growth path है।",
        },
        "loshu_diagnostic": {
            "narrative": "Lo Shu grid communication, center balance और responsibility energies के बीच कुछ gaps दिखाता है, इसलिए conscious habit design यहां जरूरी है।",
        },
        "planetary_mapping": {
            "narrative": "Primary intervention planet disciplined thinking और calmer execution की मांग कर रहा है, इसलिए remedies को daily routine से जोड़ना जरूरी है।",
        },
        "execution_plan": {
            "summary": "21-day execution plan का उद्देश्य quick motivation नहीं बल्कि measurable rhythm build करना है।",
        },
    }


def _visible_fallback_fonts(pdf_bytes: bytes) -> set[str]:
    fallback_fonts = set()
    reader = PdfReader(BytesIO(pdf_bytes))

    for page in reader.pages:
        font_resources = {
            str(name): str(font_ref.get_object().get("/BaseFont", ""))
            for name, font_ref in (page.get("/Resources", {}).get("/Font", {}) or {}).items()
        }
        content = page.get_contents()
        if not content:
            continue

        current_font = None
        stream = ContentStream(content, reader)
        for operands, operator in stream.operations:
            if operator == b"Tf":
                current_font = str(operands[0])
                continue

            if operator not in {b"Tj", b"TJ", b"'", b'"'}:
                continue

            base_font = font_resources.get(current_font, "")
            if "Helvetica" not in base_font and "Times-Roman" not in base_font:
                continue

            if operator == b"TJ":
                has_text = any(str(item).strip() for item in operands[0] if hasattr(item, "__str__"))
            else:
                has_text = bool(str(operands[-1]).strip())

            if has_text:
                fallback_fonts.add(base_font)

    return fallback_fonts


def run_hindi_report_smoke_test(output_dir: Path | None = None) -> Path:
    regular_font, bold_font = register_fonts()
    assert regular_font == "NotoSansDeva"
    assert bold_font in {"NotoSansDevaBold", "NotoSansDeva"}

    validated_payload = LifeSignifyRequest.model_validate(SAMPLE_REQUEST).model_dump(exclude_none=True)
    assert validated_payload["birth_details"]["date_of_birth"] == "1993-08-15"

    original_generator = report_ai_engine.generate_ai_narrative
    report_ai_engine.generate_ai_narrative = _stub_ai_narrative
    try:
        report = generate_life_signify_report(validated_payload, plan_name="basic")
    finally:
        report_ai_engine.generate_ai_narrative = original_generator

    summary = report.get("executive_brief", {}).get("summary", "")
    assert re.search(r"[\u0900-\u097F]", summary), "Expected Devanagari text in the executive summary."
    assert "à¤" not in str(report)
    assert report.get("primary_insight", {}).get("phase_1_diagnostic")
    assert report.get("execution_plan", {}).get("run_protocol")
    assert report.get("environment_alignment", {}).get("mobile_number_analysis")

    report_text = str(report)
    assert not re.search(r"\{[a-zA-Z0-9_]+\}", report_text)
    assert ", ," not in report_text

    pdf_buffer = generate_report_pdf(report)
    pdf_bytes = pdf_buffer.getvalue()
    assert pdf_bytes.startswith(b"%PDF")

    pdf_text = pdf_bytes.decode("latin-1", errors="ignore")
    assert "NotoSansDeva" in pdf_text
    assert not _visible_fallback_fonts(pdf_bytes)
    assert len(pdf_bytes) > 5000

    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="hindi-report-"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "hindi_sample_report.pdf"
    output_path.write_bytes(pdf_bytes)
    return output_path


def test_hindi_report_generation():
    output_path = run_hindi_report_smoke_test()
    assert output_path.exists()


if __name__ == "__main__":
    artifact_dir = ROOT / "tests" / "artifacts"
    pdf_path = run_hindi_report_smoke_test(artifact_dir)
    print(f"Hindi report generated successfully: {pdf_path}")
