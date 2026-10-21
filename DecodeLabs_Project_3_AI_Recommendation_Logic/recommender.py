"""Transparent content-based recommendation logic for the CineMatch demo."""

MOVIES = [
    {"title": "The Shawshank Redemption", "year": 1994, "genres": ["Drama"], "language": "English", "mood": ["Inspirational", "Emotional"], "rating": 9.3},
    {"title": "Inception", "year": 2010, "genres": ["Sci-Fi", "Action", "Thriller"], "language": "English", "mood": ["Mind-bending", "Adventurous"], "rating": 8.8},
    {"title": "Interstellar", "year": 2014, "genres": ["Sci-Fi", "Drama", "Adventure"], "language": "English", "mood": ["Mind-bending", "Emotional", "Inspirational"], "rating": 8.7},
    {"title": "The Dark Knight", "year": 2008, "genres": ["Action", "Crime", "Drama"], "language": "English", "mood": ["Suspenseful", "Adventurous"], "rating": 9.0},
    {"title": "Knives Out", "year": 2019, "genres": ["Mystery", "Comedy", "Crime"], "language": "English", "mood": ["Suspenseful", "Feel-good"], "rating": 7.9},
    {"title": "3 Idiots", "year": 2009, "genres": ["Comedy", "Drama"], "language": "Hindi", "mood": ["Feel-good", "Inspirational", "Emotional"], "rating": 8.4},
    {"title": "Dangal", "year": 2016, "genres": ["Drama", "Sport"], "language": "Hindi", "mood": ["Inspirational", "Emotional"], "rating": 8.3},
    {"title": "Zindagi Na Milegi Dobara", "year": 2011, "genres": ["Comedy", "Drama", "Adventure"], "language": "Hindi", "mood": ["Feel-good", "Inspirational", "Adventurous"], "rating": 8.2},
    {"title": "Drishyam", "year": 2013, "genres": ["Thriller", "Crime", "Drama"], "language": "Hindi", "mood": ["Suspenseful", "Emotional"], "rating": 8.2},
    {"title": "Andhadhun", "year": 2018, "genres": ["Thriller", "Mystery", "Crime"], "language": "Hindi", "mood": ["Mind-bending", "Suspenseful"], "rating": 8.2},
    {"title": "Coco", "year": 2017, "genres": ["Animation", "Adventure", "Drama"], "language": "English", "mood": ["Feel-good", "Emotional"], "rating": 8.4},
    {"title": "Spider-Man: Into the Spider-Verse", "year": 2018, "genres": ["Animation", "Action", "Adventure"], "language": "English", "mood": ["Adventurous", "Inspirational"], "rating": 8.4},
    {"title": "The Martian", "year": 2015, "genres": ["Sci-Fi", "Adventure", "Drama"], "language": "English", "mood": ["Inspirational", "Adventurous"], "rating": 8.0},
    {"title": "Queen", "year": 2013, "genres": ["Comedy", "Drama"], "language": "Hindi", "mood": ["Feel-good", "Inspirational"], "rating": 8.1},
    {"title": "Parasite", "year": 2019, "genres": ["Thriller", "Drama", "Comedy"], "language": "Korean", "mood": ["Mind-bending", "Suspenseful"], "rating": 8.5},
    {"title": "Your Name", "year": 2016, "genres": ["Animation", "Romance", "Fantasy"], "language": "Japanese", "mood": ["Emotional", "Mind-bending"], "rating": 8.4},
    {"title": "The Grand Budapest Hotel", "year": 2014, "genres": ["Comedy", "Adventure"], "language": "English", "mood": ["Feel-good", "Adventurous"], "rating": 8.1},
    {"title": "La La Land", "year": 2016, "genres": ["Romance", "Drama", "Music"], "language": "English", "mood": ["Emotional", "Feel-good"], "rating": 8.0},
    {"title": "The Imitation Game", "year": 2014, "genres": ["Drama", "Thriller", "History"], "language": "English", "mood": ["Inspirational", "Suspenseful"], "rating": 8.0},
    {"title": "Finding Nemo", "year": 2003, "genres": ["Animation", "Adventure", "Comedy"], "language": "English", "mood": ["Feel-good", "Adventurous"], "rating": 8.2},
]

def available_genres():
    return sorted({genre for movie in MOVIES for genre in movie["genres"]})

def available_languages():
    return sorted({movie["language"] for movie in MOVIES})

def _overlap_score(selected, item_values):
    """Return overlap ratio between selected preferences and item's attributes."""
    if not selected:
        return 0.0
    return len(set(selected) & set(item_values)) / len(set(selected))

def score_movie(movie, genres, languages, mood):
    """Weighted content similarity score from 0 to 100."""
    genre_score = _overlap_score(genres, movie["genres"])
    language_score = 1.0 if languages and movie["language"] in languages else (0.5 if not languages else 0.0)
    mood_score = 1.0 if mood == "Any mood" else (1.0 if mood in movie["mood"] else 0.0)
    rating_score = max(0.0, min(1.0, movie["rating"] / 10.0))

    weighted = (
        0.50 * genre_score
        + 0.20 * language_score
        + 0.20 * mood_score
        + 0.10 * rating_score
    )
    return round(weighted * 100, 1)

def recommend_movies(genres, languages=None, mood="Any mood", min_rating=0.0,
                     top_n=5, strict_language=False):
    """Filter and rank catalogue titles by weighted preference similarity."""
    languages = languages or []
    selected_genres = list(genres or [])
    if not selected_genres:
        return []

    candidates = []
    for original in MOVIES:
        if original["rating"] < min_rating:
            continue
        if strict_language and languages and original["language"] not in languages:
            continue
        if not set(selected_genres).intersection(original["genres"]):
            continue

        movie = dict(original)
        movie["genres"] = list(original["genres"])
        movie["mood"] = list(original["mood"])
        movie["similarity_score"] = score_movie(movie, selected_genres, languages, mood)

        matched_genres = sorted(set(selected_genres).intersection(movie["genres"]))
        reasons = [f"Matches your genre choice: {', '.join(matched_genres)}"]
        if languages and movie["language"] in languages:
            reasons.append(f"language matches ({movie['language']})")
        if mood != "Any mood" and mood in movie["mood"]:
            reasons.append(f"fits your {mood.lower()} mood")
        movie["reason"] = "; ".join(reasons) + "."
        candidates.append(movie)

    candidates.sort(key=lambda item: (item["similarity_score"], item["rating"], item["title"]), reverse=True)
    return candidates[:max(0, int(top_n))]
