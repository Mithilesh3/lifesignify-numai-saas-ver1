from pathlib import Path
from io import BytesIO
import re
import sys
import tempfile
import types

from pypdf import PdfReader

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
            raise RuntimeError("Azure OpenAI client should not be called in this smoke test.")

    openai_stub.AzureOpenAI = _DummyAzureOpenAI
    sys.modules["openai"] = openai_stub

import app.modules.reports.ai_engine as report_ai_engine
from app.modules.reports.ai_engine import generate_life_signify_report
from app.modules.reports.html_engine.engine import _build_context
from app.modules.reports.intake_schema import LifeSignifyRequest
from app.modules.reports.pdf_engine import generate_report_pdf

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
    "current_problem": "Career execution is inconsistent and financial planning discipline is weak.",
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


# Keep this stub small; deterministic interpretation engine remains primary source.
def _stub_ai_narrative(*_args, **_kwargs):
    return {
        "executive_brief": {
            "summary": "Primary deterministic signal indicates growth potential with structure-first execution.",
            "key_strength": "Adaptability with analytical clarity.",
            "key_risk": "Inconsistent financial and emotional rhythm under stress.",
            "strategic_focus": "Run a 21-day discipline protocol around decision filters.",
        },
        "primary_insight": {
            "narrative": "Core intervention should convert intelligence into repeatable behavior loops.",
        },
        "planetary_mapping": {
            "narrative": "Planetary map should be treated as a calibration model, not deterministic fate.",
        },
        "execution_plan": {
            "summary": "Execution plan focuses on install rhythm, deploy anchor, and run protocol.",
        },
    }


def _playwright_ready() -> tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - environment dependent
        return False, f"Playwright package unavailable: {exc}"

    try:  # pragma: no cover - environment dependent
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            browser.close()
        return True, ""
    except Exception as exc:
        return False, f"Chromium runtime unavailable: {exc}"


def run_hindi_report_smoke_test(output_dir: Path | None = None) -> Path:
    validated_payload = LifeSignifyRequest.model_validate(SAMPLE_REQUEST).model_dump(exclude_none=True)
    assert validated_payload["birth_details"]["date_of_birth"] == "1993-08-15"

    original_generator = report_ai_engine.generate_ai_narrative
    report_ai_engine.generate_ai_narrative = _stub_ai_narrative
    try:
        report = generate_life_signify_report(validated_payload, plan_name="basic")
    finally:
        report_ai_engine.generate_ai_narrative = original_generator

    report_text = str(report)
    assert not re.search(r"\{[a-zA-Z0-9_]+\}", report_text)
    assert ", ," not in report_text

    context = _build_context(report, watermark=False)
    assert "<svg" in context["diagrams"]["numerology_architecture"]
    assert "<svg" in context["diagrams"]["loshu_grid"]
    assert "<svg" in context["diagrams"]["structural_deficit"]
    assert "<svg" in context["diagrams"]["planetary_orbit"]
    assert context["metrics"]["radar_values_json"].startswith("[")

    ready, reason = _playwright_ready()
    if not ready:
        if "pytest" in sys.modules:
            import pytest
            pytest.skip(reason)
        raise RuntimeError(reason)

    pdf_buffer = generate_report_pdf(report)
    pdf_bytes = pdf_buffer.getvalue()

    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 6000

    reader = PdfReader(BytesIO(pdf_bytes))
    assert len(reader.pages) == 12

    text_sample = " ".join((reader.pages[index].extract_text() or "") for index in range(min(3, len(reader.pages))))
    if text_sample.strip():
        assert any(keyword in text_sample for keyword in ("Strategic", "NumAI", "Audit"))

    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="html-report-"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "hindi_sample_report.pdf"
    output_path.write_bytes(pdf_bytes)
    return output_path


def test_hindi_report_generation():
    ready, reason = _playwright_ready()
    if not ready:
        import pytest
        pytest.skip(reason)

    output_path = run_hindi_report_smoke_test()
    assert output_path.exists()


if __name__ == "__main__":
    artifact_dir = ROOT / "tests" / "artifacts"
    ready, reason = _playwright_ready()
    if not ready:
        print(f"Playwright check failed: {reason}")
        sys.exit(0)

    pdf_path = run_hindi_report_smoke_test(artifact_dir)
    print(f"Hindi HTML report generated successfully: {pdf_path}")


