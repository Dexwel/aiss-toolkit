import pandas as pd
import pytest
from aiss import logic
from aiss.data import AUDIT_ITEMS, MAX_AUDIT_SCORE, TIERS


def test_max_score_matches_items():
    assert sum(max(p for _, p in opts) for _, _, opts in AUDIT_ITEMS) == MAX_AUDIT_SCORE == 20


@pytest.mark.parametrize("score,tier", [(0, 0), (5, 0), (6, 1), (10, 1), (11, 2), (15, 2), (16, 3), (20, 3)])
def test_tier_from_score(score, tier):
    assert logic.tier_from_score(score) == tier


def test_triage_follows_figure_5():
    assert logic.triage_tier(False, True, True) == 0
    assert logic.triage_tier(True, False, True) == 1
    assert logic.triage_tier(True, True, False) == 2
    assert logic.triage_tier(True, True, True) == 3


def test_planning_tier_is_conservative():
    assert logic.planning_tier(3, 1) == 1


def test_flags_no_lead_teacher():
    assert any("lead teacher" in f for f in logic.audit_flags({6: 0, 8: 2}, 1))


def test_cost_per_student_matches_paper():
    df = pd.DataFrame({"Tier": [TIERS[t]["name"] for t in TIERS], "Setup": [TIERS[t]["setup"] for t in TIERS],
                       "Running": [TIERS[t]["running"] for t in TIERS], "Students": [TIERS[t]["students"] for t in TIERS]})
    r = logic.cost_table(df, 3, 0.0)
    assert [round(x) for x in r["Cost per student per year"]] == [4125, 4017, 5540, 5655]
    assert r["Total over horizon"].iloc[0] == 165_000 + 3 * 165_000


def test_analyze_gain_basic():
    df = pd.DataFrame({"baseline": [8, 10, 9, 11, 7, 12], "endline": [12, 13, 12, 15, 10, 14]})
    r = logic.analyze_gain(df, 20)
    assert r["n"] == 6 and r["mean_gain"] == pytest.approx(3.1666, abs=1e-3)
    assert r["p"] < 0.05 and r["cohens_dz"] > 0.8 and r["pct_improved"] == 100


def test_analyze_gain_needs_two():
    with pytest.raises(ValueError):
        logic.analyze_gain(pd.DataFrame({"baseline": [5], "endline": [7]}))


def test_analyze_gain_zero_variance():
    r = logic.analyze_gain(pd.DataFrame({"baseline": [5, 6, 7], "endline": [7, 8, 9]}))
    assert r["mean_gain"] == 2 and r["p"] == 0.0


def test_participation_gap():
    g = logic.participation_gap({"F": 10, "M": 30}, {"F": 200, "M": 200}, 10)
    assert g.loc[g.Group == "F", "Status"].iloc[0] == "Review"


def test_rubric_bands():
    assert logic.rubric_band(5) == "Emerging" and logic.rubric_band(8) == "Proficient" and logic.rubric_band(15) == "Advanced"
    assert logic.rubric_total({"a": 2, "b": 3}) == 5


def test_portfolio_completion():
    df = pd.DataFrame({"x": [True, True], "y": [True, False]})
    assert logic.portfolio_completion(df, ["x", "y"]) == (1, 50.0)


def test_consent_letter_mentions_online():
    assert "online AI tools" in logic.consent_letter("S", "P", "C", True)
    assert "no online tools" in logic.consent_letter("S", "P", "C", False)
