import unittest
from recommender import recommend_movies, score_movie, MOVIES

class RecommendationTests(unittest.TestCase):
    def test_empty_genres_returns_empty(self):
        self.assertEqual(recommend_movies([], ["English"]), [])

    def test_only_matching_genres_are_returned(self):
        results = recommend_movies(["Sci-Fi"], ["English"], "Any mood", 0, 8)
        self.assertTrue(results)
        self.assertTrue(all("Sci-Fi" in movie["genres"] for movie in results))

    def test_minimum_rating_filter(self):
        results = recommend_movies(["Drama"], ["English"], "Any mood", 9.0, 8)
        self.assertTrue(all(movie["rating"] >= 9.0 for movie in results))

    def test_strict_language_filter(self):
        results = recommend_movies(["Drama"], ["Hindi"], "Any mood", 0, 20, True)
        self.assertTrue(all(movie["language"] == "Hindi" for movie in results))

    def test_scores_are_in_range(self):
        results = recommend_movies(["Drama"], ["English"], "Any mood", 0, 20)
        self.assertTrue(all(0 <= movie["similarity_score"] <= 100 for movie in results))

    def test_results_sorted_by_score(self):
        results = recommend_movies(["Drama", "Thriller"], ["English"], "Suspenseful", 0, 20)
        scores = [movie["similarity_score"] for movie in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

if __name__ == "__main__":
    unittest.main()
