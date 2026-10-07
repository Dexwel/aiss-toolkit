"""Pure calculation functions (no Streamlit imports) so they can be unit-tested."""
from __future__ import annotations
import math
import pandas as pd
from .data import MAX_AUDIT_SCORE


def triage_tier(power: bool, computers: bool, internet: bool) -> int:
    """Figure 5 decision procedure: power -> computers -> internet."""
    if not power:
        return 0
    if not computers:
        return 1
    if not internet:
        return 2
    return 3


def tier_from_score(score: int) -> int:
    if score <= 5:
        return 0
    if score <= 10:
        return 1
    if score <= 15:
        return 2
    return 3


def audit_score(answers: dict) -> int:
    """answers maps item id -> points awarded."""
    return int(sum(answers.values()))


def audit_flags(answers: dict, tier: int) -> list:
    flags = []
    if answers.get(6, 0) == 0:
        flags.append("No AI lead teacher: the school is not ready at any tier until one is appointed.")
    if answers.get(8, 0) == 0:
        flags.append("No documented funding for Years 2 and 3: the framework advises against starting until this is agreed.")
    if tier >= 2 and answers.get(9, 0) == 0:
        flags.append("Devices without an assigned technician risk becoming idle equipment.")
    if tier >= 2 and answers.get(10, 1) == 0:
        flags.append("History of abandoned technology: add a maintenance plan before deploying more devices.")
    return flags


def planning_tier(score_tier: int, triage: int) -> int:
    """Use the lower (more conservative) of the two methods."""
    return min(score_tier, triage)


def cost_table(df: pd.DataFrame, years: int = 3, inflation: float = 0.0) -> pd.DataFrame:
    """df columns: Tier, Setup, Running, Students. Returns cost metrics."""
    out = df.copy()
    out["Students"] = out["Students"].astype(float).replace(0, float("nan"))
    out["Cost per student per year"] = out["Running"] / out["Students"]
    total = []
    for _, r in out.iterrows():
        t = float(r["Setup"])
        for y in range(years):
            t += float(r["Running"]) * ((1 + inflation) ** y)
        total.append(t)
    out["Total over horizon"] = total
    out["Cost per student over horizon"] = out["Total over horizon"] / (out["Students"] * years)
    return out


def effect_label(dz: float) -> str:
    a = abs(dz)
    if a < 0.2:
        return "negligible"
    if a < 0.5:
        return "small"
    if a < 0.8:
        return "medium"
    return "large"


def analyze_gain(df: pd.DataFrame, max_score: float = 20.0) -> dict:
    """Paired baseline/endline analysis. df needs numeric 'baseline' and 'endline'."""
    from scipy import stats
    d = df[["baseline", "endline"]].apply(pd.to_numeric, errors="coerce").dropna()
    n = len(d)
    if n < 2:
        raise ValueError("At least two students with both scores are required.")
    diff = d["endline"] - d["baseline"]
    mean_diff = float(diff.mean())
    sd = float(diff.std(ddof=1))
    if sd == 0:
        t_stat = float("inf") if mean_diff != 0 else 0.0
        p = 0.0 if mean_diff != 0 else 1.0
        dz = float("inf") if mean_diff != 0 else 0.0
        ci = (mean_diff, mean_diff)
    else:
        res = stats.ttest_rel(d["endline"], d["baseline"])
        t_stat, p = float(res.statistic), float(res.pvalue)
        dz = mean_diff / sd
        se = sd / math.sqrt(n)
        tcrit = stats.t.ppf(0.975, n - 1)
        ci = (mean_diff - tcrit * se, mean_diff + tcrit * se)
    try:
        w_p = float(stats.wilcoxon(d["endline"], d["baseline"]).pvalue) if (diff != 0).any() else 1.0
    except ValueError:
        w_p = float("nan")
    return {
        "n": n, "baseline_mean": float(d["baseline"].mean()), "endline_mean": float(d["endline"].mean()),
        "mean_gain": mean_diff, "gain_pct_points": mean_diff / max_score * 100,
        "pct_improved": float((diff > 0).mean() * 100), "pct_declined": float((diff < 0).mean() * 100),
        "t": t_stat, "p": p, "wilcoxon_p": w_p, "cohens_dz": float(dz),
        "ci_low": float(ci[0]), "ci_high": float(ci[1]), "effect_label": effect_label(dz),
    }


def participation_gap(club_counts: dict, school_counts: dict, threshold_pp: float = 10.0) -> pd.DataFrame:
    """Compare club composition with the school roll (fairness check)."""
    ct, st_ = sum(club_counts.values()), sum(school_counts.values())
    rows = []
    for g in school_counts:
        cp = club_counts.get(g, 0) / ct * 100 if ct else 0.0
        sp = school_counts[g] / st_ * 100 if st_ else 0.0
        gap = cp - sp
        rows.append({"Group": g, "Club %": round(cp, 1), "School %": round(sp, 1),
                     "Gap (pp)": round(gap, 1), "Status": "Review" if abs(gap) > threshold_pp else "Balanced"})
    return pd.DataFrame(rows)


def rubric_total(scores: dict) -> int:
    return int(sum(scores.values()))


def rubric_band(total: int) -> str:
    if total <= 7:
        return "Emerging"
    if total <= 11:
        return "Proficient"
    return "Advanced"


def portfolio_completion(df: pd.DataFrame, item_cols: list) -> tuple:
    if df.empty:
        return 0, 0.0
    complete = int(df[item_cols].all(axis=1).sum())
    return complete, complete / len(df) * 100


def audit_report_md(school, score, score_tier, triage, plan, answers_text, flags, actions) -> str:
    lines = [f"# AISS School Audit Report: {school or 'Unnamed school'}", "",
             f"- Audit score: **{score} / {MAX_AUDIT_SCORE}** (score-based tier: {score_tier})",
             f"- Quick triage tier (power, computers, internet): {triage}",
             f"- **Recommended planning tier: Tier {plan}** (the lower of the two methods)", "",
             "## Responses", "", "| Item | Response | Points |", "|---|---|---|"]
    lines += [f"| {q} | {a} | {p} |" for q, a, p in answers_text]
    lines += ["", "## Readiness flags", ""] + ([f"- {f}" for f in flags] or ["- None"])
    lines += ["", "## Recommended next actions", ""] + [f"- {a}" for a in actions]
    lines += ["", "_Generated with the AISS Framework toolkit. Planning aid only; it has not been empirically validated._"]
    return "\n".join(lines)


def consent_letter(school: str, principal: str, contact: str, uses_online: bool) -> str:
    online = ("Some lessons may use free online AI tools under teacher supervision."
              if uses_online else "Lessons use paper, cards and discussion; no online tools are planned.")
    return f"""{school or '[School name]'}

Dear Parent or Guardian,

This school is introducing lessons in artificial intelligence, the technology behind predictive text and bank fraud alerts. Most lessons use paper and cards; some may use free computer tools. {online}

Please tick each item you agree to. You may consent to some and not others.

[ ] My child may take part in the AI lessons and club.
[ ] My child may use free online AI tools under teacher supervision.
[ ] My child's work may be shown anonymously as an example of outcomes.

No personal information beyond that held by the school will be collected, and your child's photograph and full name will not be entered into any online tool. Consent may be withdrawn at any time, without disadvantage, by written notice to the principal.

Learner: ____________________   Class: ________
Parent/guardian name: ____________________
Signature: ____________________   Date: ____________

Principal: {principal or '[Name]'}   Contact: {contact or '[Phone/email]'}
"""
