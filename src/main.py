"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 7.0

# Taste profiles: categorical prefs (exact match) + numeric targets (closeness)
PROFILES = {
    "pop / happy (default)": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "target_danceability": 0.80,
        "target_acousticness": 0.20,
        "target_tempo_bpm": 120,
    },
    "lofi / chill": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
        "target_tempo_bpm": 80,
    },
}


def print_recommendations(name: str, recommendations: list) -> None:
    print("=" * 60)
    print(f"Top {len(recommendations)} for profile: {name}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   [{song['genre']} / {song['mood']}]  Score: {score:.2f} / {MAX_SCORE:.1f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, recommendations)


if __name__ == "__main__":
    main()
