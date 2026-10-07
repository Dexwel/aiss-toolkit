# AISS Toolkit

**AI Implementation Framework for Nigerian Secondary Schools** as a web app.
Built with [Streamlit](https://streamlit.io). Helps teachers, principals and education officials
plan, teach, assess and cost AI education in any school, from paper-only classrooms to online labs.

> Core idea: every student learns the same AI skills; only the delivery changes.

## Features

| Page | What it does |
|---|---|
| Home | Framework overview with all eight figures |
| School Audit | 10-item audit plus quick triage gives your planning tier, readiness flags and a downloadable report |
| Curriculum Planner | 12-week plan matched to your tier, card-sorting lesson, progression and equity guidance |
| Cost Calculator | Editable costs, inflation, multi-year totals, "what can my budget start?" |
| Assessment Analyzer | Baseline vs endline: mean gain, 95% CI, paired t-test, Wilcoxon, Cohen's dz; club vs school fairness check |
| Project Rubric | 5-criterion rubric scorer with bands and CSV export |
| Portfolio & Consent | Six-item portfolio tracker; editable parental consent letter |
| M&E Dashboard | Five programme indicators with Met / Not met status |
| About | Framework summary, limitations, privacy, references |

No data is stored by the app. Users download their results as CSV/Markdown/TXT.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Deploy: GitHub, then Streamlit Community Cloud

1. Create a new **public** GitHub repository (e.g. `aiss-toolkit`) and push this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AISS Toolkit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/aiss-toolkit.git
   git push -u origin main
   ```
2. Go to <https://share.streamlit.io>, sign in with GitHub and click **Create app**.
3. Choose the repository, branch `main`, and main file path `app.py`.
4. Under **Advanced settings**, pick Python 3.11 or 3.12. Click **Deploy**.
5. Optional: set a custom subdomain, e.g. `aiss-toolkit.streamlit.app`.

Streamlit Cloud redeploys automatically on every push to `main`.

## Project structure

```
app.py                      Home page
pages/                      One file per tool page (numbered for sidebar order)
aiss/data.py                Framework content (tiers, audit items, curriculum, rubric, references)
aiss/logic.py               Pure calculation functions (unit-tested)
aiss/ui.py                  Shared Streamlit helpers
assets/                     Framework figures
tests/                      Unit tests and page smoke tests
.streamlit/config.toml      Theme and settings
.github/workflows/ci.yml    Runs tests on each push
```

## Customising

- Change costs, audit items or curriculum text in `aiss/data.py`; no page code changes needed.
- Add a page by creating `pages/9_Your_Page.py` and calling `ui.setup("Title", "icon")` first.

## Limitations

The framework is built from literature and national data and has **not yet been empirically validated**.
Cost figures are planning estimates. Verify the references in `aiss/data.py` against the original
sources before formal citation. This toolkit is a planning aid, not legal advice.

## Licence

Code: MIT (edit `LICENSE` with your name). Figures and framework text are your own work; add a content
licence (e.g. CC BY 4.0) if you want others to reuse them.
