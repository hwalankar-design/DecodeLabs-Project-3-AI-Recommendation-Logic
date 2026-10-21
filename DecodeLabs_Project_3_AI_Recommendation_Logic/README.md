# DecodeLabs Project 3 — AI Recommendation Logic

**App:** CineMatch — AI Recommendation Studio  
**Stack:** Python, Streamlit, Pandas, unittest  
**Approach:** Explainable content-based recommendation using weighted similarity.

## Project requirements addressed
1. Takes user preferences: genres, languages, mood, minimum rating and result count.
2. Matches preferences using a weighted similarity formula.
3. Displays ranked recommendations, similarity percentages, explanations and a CSV export.

## Similarity formula
- Genre overlap: 50%
- Language match: 20%
- Mood match: 20%
- Rating normalized to 0–1: 10%

`score = 100 × (0.50 × genre + 0.20 × language + 0.20 × mood + 0.10 × rating)`

This is a small demonstration catalogue with manually entered sample metadata; it does not use a trained model or live movie database.

## Setup (Windows / VS Code)
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Run tests
From the project root:
```powershell
python -m unittest discover -s tests -v
```

## Suggested manual checks
- Select Drama + English and press Find my matches.
- Turn on exact language matching and choose Hindi; results should be Hindi only.
- Raise the minimum rating to 9.0; results should have ratings >= 9.0.
- Clear all genres and click Find my matches; the app should ask you to select a genre.
- Download the results CSV and confirm it contains the ranked recommendations.

## Submission checklist
- Run the app and capture screenshots of preferences and recommendations.
- Run automated tests and keep the passing terminal output.
- Upload the complete project folder or a ZIP if the portal asks for an archive.
- Include this README and a short explanation of the scoring formula.
- Follow the exact submission format and deadline given by DecodeLabs; the PDF does not specify a particular upload URL or format.
