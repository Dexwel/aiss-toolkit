"""Smoke-test every page with Streamlit's AppTest: each must render without exceptions."""
import sys
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
PAGES = ["app.py"] + sorted(str(p.relative_to(ROOT)) for p in (ROOT / "pages").glob("*.py"))


@pytest.mark.parametrize("page", PAGES)
def test_page_renders(page):
    at = AppTest.from_file(str(ROOT / page), default_timeout=30).run()
    assert not at.exception, [e.value for e in at.exception]


def test_audit_flow_sets_tier():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    at.switch_page("pages/1_School_Audit.py").run()
    at.button[0].click().run()
    assert not at.exception
    assert "plan_tier" in at.session_state
