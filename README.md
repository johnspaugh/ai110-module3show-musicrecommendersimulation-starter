# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders


These are the songs.csv columns of data:
id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness

And this recommander app will take in the users profile as measurement on what to recommand
The app will first load all the songs from songs.csv, then use the measurements to weigh/sort all
the songs' columns of data by the user's profile given. Then take the top k recommandations to show the users.



---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

### Songs and User Profile

- **Song features:** `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` (plus `id`, `title`, `artist`). The catalog has 18 songs.
- **UserProfile:** one favorite genre, one favorite mood, and a target value for energy, valence, danceability, acousticness and tempo (the example is lofi / chill / energy 0.40).
- **Flow:** load every song from `data/songs.csv`, score each one against the profile, sort by score, and return the top `k` with a short explanation of why each was picked.

### Data Flow

```
INPUT                       PROCESS (the loop)                          OUTPUT
─────                       ──────────────────                          ──────
user_prefs  ──┐
 genre, mood, │
 target_*     │
              ▼
data/songs.csv ─► load_songs() ─► list of song dicts (18)
                                        │
                       for each song ◄──┘
                              │
                              ▼
                  score_song(user_prefs, song)
                    (see Algorithm Recipe below)
                              │
                              ▼
                  (song, score, explanation)    ← one tuple per song
                              │
                              ▼
              collect all tuples ─► sort by score, descending
                                              │
                                              ▼
                                    take first k ─► Top K recommendations
```

### Algorithm Recipe

Each song gets a score out of **7.0**. Songs are scored independently, sorted high to low, and the top `k` are returned with an explanation.

| Rule | Points | How it's computed |
|---|---|---|
| Genre match | +2.0 | exact match with `favorite_genre` |
| Mood match | +1.0 | exact match with `favorite_mood` |
| Energy closeness | up to +1.5 | `1.5 * (1 - abs(song.energy - target_energy))` |
| Acousticness closeness | up to +1.0 | `1.0 * (1 - abs(song.acousticness - target_acousticness))` |
| Valence closeness | up to +0.5 | `0.5 * (1 - abs(song.valence - target_valence))` |
| Danceability closeness | up to +0.5 | `0.5 * (1 - abs(song.danceability - target_danceability))` |
| Tempo closeness | up to +0.5 | `0.5 * (1 - min(abs(song.tempo_bpm - target_tempo_bpm) / 100, 1))` |

Why these weights:
- **Genre (2.0) > mood (1.0):** genre is the broader and more stable preference, so it counts double. Mood is more situational. Together they are 3.0 of 7.0, so a song can't win on labels alone.
- **Energy (1.5) is the strongest numeric feature:** it separates "intense rock" from "chill lofi" best (about 0.3 vs 0.9). Acousticness (1.0) is next because it also splits the two groups.
- **Valence, danceability and tempo (0.5 each)** are tie-breakers, because most songs in the catalog score similarly on them. Tempo is divided by 100 so BPM is on the same 0–1 scale as the other features.
- **Closeness, not "higher is better":** a user who wants 0.40 energy should not get a 0.95 energy song just because it's higher.

### Expected Biases

- **Genre can over-prioritize:** genre is worth 2.0 points, so a song in the favorite genre with a poor numeric fit can outrank a song in another genre that matches the user's mood, energy and acousticness almost exactly. A lofi fan may never see a perfect-fit jazz track.
- **Exact matching has no partial credit:** jazz vs. lofi, or chill vs. relaxed, score as completely different, even though listeners treat them as close.
- **Catalog imbalance:** lofi has 3 songs, while most other genres have 1. Lofi-leaning profiles get more good options than users who prefer country, metal or folk.
- **One taste per user:** a single genre and mood, with one target value per feature, can't represent someone who likes both calm acoustic music and high-energy workouts.
- **Energy and acousticness dominate the numbers:** they carry 2.5 of the 3.5 numeric points, so valence, danceability and tempo rarely change the ranking.
- **Closeness favors the middle:** a user with an extreme target (energy 0.95) has few songs close to it, while mid-range targets (0.5–0.6) are close to many songs, so mid-range profiles get more evenly ranked results.
- **Small, made-up data:** 18 songs with hand-picked feature values, so results reflect the dataset, not real listening behavior.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` on the 18-song catalog (default pop / happy profile, then lofi / chill):

```
Loading songs from data/songs.csv...
Loaded songs: 18

============================================================
Top 5 for profile: pop / happy (default)
============================================================

1. Sunrise City - Neon Echo
   [pop / happy]  Score: 6.92 / 7.0
     - genre match (+2.0)
     - mood match (+1.0)
     - energy close to target (+1.47)
     - acousticness close to target (+0.98)
     - valence close to target (+0.48)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.49)

2. Gym Hero - Max Pulse
   [pop / intense]  Score: 5.54 / 7.0
     - genre match (+2.0)
     - energy close to target (+1.30)
     - acousticness close to target (+0.85)
     - valence close to target (+0.48)
     - danceability close to target (+0.46)
     - tempo_bpm close to target (+0.44)

3. Rooftop Lights - Indigo Parade
   [indie pop / happy]  Score: 4.76 / 7.0
     - mood match (+1.0)
     - energy close to target (+1.44)
     - acousticness close to target (+0.85)
     - valence close to target (+0.49)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.48)

4. Night Drive Loop - Neon Echo
   [synthwave / moody]  Score: 3.67 / 7.0
     - energy close to target (+1.42)
     - acousticness close to target (+0.98)
     - valence close to target (+0.34)
     - danceability close to target (+0.46)
     - tempo_bpm close to target (+0.45)

5. Concrete Crown - Lyric Vandal
   [hip hop / confident]  Score: 3.65 / 7.0
     - energy close to target (+1.47)
     - acousticness close to target (+0.92)
     - valence close to target (+0.41)
     - danceability close to target (+0.47)
     - tempo_bpm close to target (+0.38)

============================================================
Top 5 for profile: lofi / chill
============================================================

1. Midnight Coding - LoRoom
   [lofi / chill]  Score: 6.90 / 7.0
     - genre match (+2.0)
     - mood match (+1.0)
     - energy close to target (+1.47)
     - acousticness close to target (+0.96)
     - valence close to target (+0.49)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.49)

2. Library Rain - Paper Lanterns
   [lofi / chill]  Score: 6.75 / 7.0
     - genre match (+2.0)
     - mood match (+1.0)
     - energy close to target (+1.42)
     - acousticness close to target (+0.89)
     - valence close to target (+0.49)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.46)

3. Focus Flow - LoRoom
   [lofi / focused]  Score: 5.96 / 7.0
     - genre match (+2.0)
     - energy close to target (+1.50)
     - acousticness close to target (+0.97)
     - valence close to target (+0.49)
     - danceability close to target (+0.50)
     - tempo_bpm close to target (+0.50)

4. Spacewalk Thoughts - Orbit Bloom
   [ambient / chill]  Score: 4.42 / 7.0
     - mood match (+1.0)
     - energy close to target (+1.32)
     - acousticness close to target (+0.83)
     - valence close to target (+0.46)
     - danceability close to target (+0.41)
     - tempo_bpm close to target (+0.40)

5. Coffee Shop Stories - Slow Stereo
   [jazz / relaxed]  Score: 3.67 / 7.0
     - energy close to target (+1.46)
     - acousticness close to target (+0.86)
     - valence close to target (+0.43)
     - danceability close to target (+0.47)
     - tempo_bpm close to target (+0.45)
```

The pop / happy result is what the recipe predicts: Sunrise City (pop, happy) wins with nearly the full 7.0. Gym Hero is next on genre alone despite the wrong mood, and Rooftop Lights follows on mood alone. The last two have no genre or mood match and rank on numeric closeness only.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



