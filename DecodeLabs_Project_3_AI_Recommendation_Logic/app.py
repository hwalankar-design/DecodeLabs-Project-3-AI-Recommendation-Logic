import streamlit as st
import pandas as pd
from recommender import MOVIES, recommend_movies, available_genres, available_languages

st.set_page_config(
    page_title="CineMatch | AI Recommendation Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root { --gold: #d6b779; --ink: #101114; --panel: #191b20; --muted: #a7a9b1; }
.stApp { background: radial-gradient(circle at 80% 0%, #29251e 0, #111216 38%, #0d0e11 100%); color: #f5f2eb; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }
.block-container { padding-top: 1.8rem; max-width: 1400px; }
section[data-testid="stSidebar"] { background: #15161a; border-right: 1px solid #303036; }
.hero { padding: 1.5rem 0 1rem 0; }
.eyebrow { color: #d6b779; letter-spacing: .18em; font-size: .76rem; font-weight: 700; text-transform: uppercase; }
.hero h1 { font-size: clamp(2.5rem, 5vw, 4.1rem); line-height: 1.04; margin: .4rem 0; color: #f6f0e4; }
.hero p { color: #b6b5b1; font-size: 1.05rem; max-width: 760px; }
.metric-card { background: linear-gradient(135deg,#202127,#17181d); border: 1px solid #34343a; border-radius: 16px; padding: 17px 18px; min-height: 104px; }
.metric-label { color: #a7a9b1; font-size: .82rem; }
.metric-value { color: #f6f0e4; font-size: 1.8rem; font-weight: 700; margin-top: 5px; }
.movie-card { height: 100%; background: linear-gradient(160deg,#202127,#15161a); border: 1px solid #34343a; border-radius: 18px; padding: 20px; margin-bottom: 14px; }
.movie-top { display:flex; justify-content:space-between; gap:12px; align-items:start; }
.movie-title { color:#f7f1e7; font-family:'Playfair Display',serif; font-size:1.35rem; font-weight:700; }
.movie-year { color:#c7c0b3; font-size:.86rem; white-space:nowrap; }
.pill { display:inline-block; border:1px solid #65583e; background:#30291d; color:#e3c98e; border-radius:999px; padding:4px 9px; margin:4px 4px 0 0; font-size:.74rem; }
.score { color:#e3c98e; font-size:1.15rem; font-weight:700; }
.muted { color:#a7a9b1; font-size:.9rem; }
.reason { color:#d5d0c6; font-size:.9rem; padding-top:8px; }
.stButton > button { border-radius: 10px; font-weight: 700; }
div[data-testid="stProgress"] > div > div { background-color: #d6b779; }
[data-testid="stMetricValue"] { color: #e3c98e; }
hr { border-color: #33343a; }
</style>
""", unsafe_allow_html=True)

if "last_results" not in st.session_state:
    st.session_state.last_results = None

with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    st.caption("AI RECOMMENDATION STUDIO")
    st.markdown("---")
    st.markdown("### Tune your taste")
    genres = st.multiselect(
        "Choose genres",
        options=available_genres(),
        default=["Drama", "Thriller"],
        help="Select one or more genres you enjoy."
    )
    languages = st.multiselect(
        "Preferred language",
        options=available_languages(),
        default=["English"],
    )
    mood = st.selectbox(
        "What are you in the mood for?",
        ["Any mood", "Feel-good", "Mind-bending", "Inspirational", "Suspenseful", "Emotional", "Adventurous"]
    )
    min_rating = st.slider("Minimum audience rating", min_value=6.0, max_value=9.0, value=7.0, step=0.5)
    top_n = st.slider("Number of recommendations", min_value=3, max_value=8, value=5)
    strict_language = st.checkbox("Prefer exact language matches", value=False)
    recommend_clicked = st.button("✨ Find my matches", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("Demo catalogue • Offline-ready • No account required")

st.markdown("""
<div class="hero">
  <div class="eyebrow">PERSONALIZED DISCOVERY · PROJECT 03</div>
  <h1>Find your next<br>favourite story.</h1>
  <p>Tell CineMatch what you love. A transparent similarity algorithm ranks titles by genre, language, mood and rating — with a score you can understand.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
for col, label, value in [
    (m1, "TITLES IN CATALOGUE", f"{len(MOVIES):02d}"),
    (m2, "MATCHING SIGNALS", "04"),
    (m3, "SCORING METHOD", "0–100"),
]:
    col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

if recommend_clicked:
    if not genres:
        st.warning("Please select at least one genre so the system can understand your preferences.")
        st.session_state.last_results = None
    else:
        st.session_state.last_results = recommend_movies(
            genres=genres,
            languages=languages,
            mood=mood,
            min_rating=min_rating,
            top_n=top_n,
            strict_language=strict_language,
        )

st.markdown("---")
st.markdown("## Your recommendations")
st.caption("Ranked by preference similarity. Scores describe how closely each title matches your selected profile.")

results = st.session_state.last_results
if results is None:
    st.info("Choose your preferences in the sidebar, then select **Find my matches** to generate your personalized list.")
else:
    if not results:
        st.warning("No titles match those filters. Try lowering the minimum rating or turning off exact language matching.")
    else:
        best = results[0]
        a, b = st.columns([2, 1])
        with a:
            st.markdown(f"**Best match:** {best['title']} ({best['year']})")
            st.markdown(f"<span class='score'>{best['similarity_score']:.0f}% match</span> · {best['rating']:.1f}/10 rating", unsafe_allow_html=True)
        with b:
            st.metric("Results found", len(results))
        st.markdown("")
        cols = st.columns(2)
        for idx, movie in enumerate(results):
            with cols[idx % 2]:
                genre_pills = "".join(f"<span class='pill'>{g}</span>" for g in movie["genres"])
                st.markdown(f"""
                <div class="movie-card">
                  <div class="movie-top">
                    <div class="movie-title">{movie['title']}</div>
                    <div class="movie-year">{movie['year']}</div>
                  </div>
                  <div class="muted">{movie['language']} · ★ {movie['rating']:.1f}/10</div>
                  <div style="margin:10px 0 8px">{genre_pills}</div>
                  <div class="score">{movie['similarity_score']:.0f}% similarity</div>
                  <div class="reason">{movie['reason']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(int(movie["similarity_score"]), text=f"Preference match: {movie['similarity_score']:.0f}%")
        export_df = pd.DataFrame(results)
        export_cols = ["title", "year", "genres", "language", "mood", "rating", "similarity_score", "reason"]
        export_df = export_df[export_cols]
        export_df["genres"] = export_df["genres"].apply(lambda x: ", ".join(x))
        st.download_button(
            "⬇️ Download recommendations as CSV",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="cinematch_recommendations.csv",
            mime="text/csv",
        )

with st.expander("How does the similarity score work?"):
    st.markdown("""
    CineMatch uses a simple, explainable weighted score — it does not train a machine-learning model.

    - **Genre match (50%)**: overlap between your selected genres and a movie's genres.
    - **Language match (20%)**: whether the movie language matches your choices.
    - **Mood match (20%)**: whether the movie fits the selected mood.
    - **Rating score (10%)**: normalized audience rating.

    The weighted score is converted to a percentage and titles are ranked from highest to lowest. The minimum rating and optional exact-language setting are filters applied before ranking.
    """)

st.markdown("---")
st.markdown("<div class='muted'>DecodeLabs · Artificial Intelligence Project 3 · AI Recommendation Logic</div>", unsafe_allow_html=True)
