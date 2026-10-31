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

The default pop / happy and lofi / chill runs are in *Sample Recommendation Output* above. Below are a third normal profile and three adversarial profiles, run with `python -m src.main`.

### Deep Intense Rock

```
Top 5 for profile: deep intense rock

1. Storm Runner - Voltline
   [rock / intense]  Score: 6.96 / 7.0
     - genre match (+2.0)
     - mood match (+1.0)
     - energy close to target (+1.48)
     - acousticness close to target (+1.00)
     - valence close to target (+0.48)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.49)

2. Gym Hero - Max Pulse
   [pop / intense]  Score: 4.57 / 7.0
     - mood match (+1.0)
     - energy close to target (+1.48)
     - acousticness close to target (+0.95)
     - valence close to target (+0.34)
     - danceability close to target (+0.39)
     - tempo_bpm close to target (+0.41)

3. Iron Requiem - Black Cathedral
   [metal / angry]  Score: 3.58 / 7.0
     - energy close to target (+1.43)
     - acousticness close to target (+0.94)
     - valence close to target (+0.40)
     - danceability close to target (+0.40)
     - tempo_bpm close to target (+0.41)

4. Neon Pulse - Circuit Bloom
   [edm / euphoric]  Score: 3.45 / 7.0
     - energy close to target (+1.47)
     - acousticness close to target (+0.93)
     - valence close to target (+0.29)
     - danceability close to target (+0.37)
     - tempo_bpm close to target (+0.39)

5. Night Drive Loop - Neon Echo
   [synthwave / moody]  Score: 3.36 / 7.0
     - energy close to target (+1.24)
     - acousticness close to target (+0.88)
     - valence close to target (+0.48)
     - danceability close to target (+0.46)
     - tempo_bpm close to target (+0.30)
```

Works as intended: Storm Runner matches on everything (6.96 / 7.0). Gym Hero is second on mood and energy alone. Iron Requiem (metal / angry) is a near-perfect fit musically but gets no label points, because metal is not "rock" and angry is not "intense".

### Adversarial 1: sad but high energy (genre and mood not in the catalog)

Profile: genre `blues`, mood `sad`, energy 0.90, valence 0.15, acousticness 0.90.

```
Top 5 for profile: ADVERSARIAL: sad but high energy (genre/mood not in catalog)

1. Hollow Porch - Juniper Vale
   [folk / wistful]  Score: 2.93 / 7.0
     - energy close to target (+0.64)
     - acousticness close to target (+0.99)
     - valence close to target (+0.38)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.43)

2. Dust Road Home - Willow Creek
   [country / nostalgic]  Score: 2.87 / 7.0
     - energy close to target (+0.98)
     - acousticness close to target (+0.84)
     - valence close to target (+0.23)
     - danceability close to target (+0.47)
     - tempo_bpm close to target (+0.36)

3. Library Rain - Paper Lanterns
   [lofi / chill]  Score: 2.86 / 7.0
     - energy close to target (+0.67)
     - acousticness close to target (+0.96)
     - valence close to target (+0.28)
     - danceability close to target (+0.46)
     - tempo_bpm close to target (+0.49)

4. Focus Flow - LoRoom
   [lofi / focused]  Score: 2.81 / 7.0
     - energy close to target (+0.75)
     - acousticness close to target (+0.88)
     - valence close to target (+0.28)
     - danceability close to target (+0.45)
     - tempo_bpm close to target (+0.45)

5. Coffee Shop Stories - Slow Stereo
   [jazz / relaxed]  Score: 2.79 / 7.0
     - energy close to target (+0.70)
     - acousticness close to target (+0.99)
     - valence close to target (+0.22)
     - danceability close to target (+0.48)
     - tempo_bpm close to target (+0.40)
```

Nothing matches a label, so the best score is only 2.93 / 7.0, yet the results look just as confident as a good match. Because acousticness (up to 1.0) pulls one way and energy (up to 1.5) the other, the top 5 are quiet acoustic songs (energy 0.33-0.55) for a user who asked for energy 0.90. The songs that actually fit "sad and intense" (Iron Requiem, valence 0.25, energy 0.97; Sonata for Rain, valence 0.30) are not in the top 5.

### Adversarial 2: classical at the gym (labels vs. sound conflict)

Profile: genre `classical`, mood `euphoric`, energy 0.95, acousticness 0.95.

```
Top 5 for profile: ADVERSARIAL: classical at the gym (labels vs. sound conflict)

1. Neon Pulse - Circuit Bloom
   [edm / euphoric]  Score: 4.05 / 7.0
     - mood match (+1.0)
     - energy close to target (+1.48)
     - acousticness close to target (+0.08)
     - valence close to target (+0.49)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.50)

2. Sonata for Rain - Elise Marchetti
   [classical / melancholic]  Score: 3.97 / 7.0
     - genre match (+2.0)
     - energy close to target (+0.41)
     - acousticness close to target (+1.00)
     - valence close to target (+0.20)
     - danceability close to target (+0.17)
     - tempo_bpm close to target (+0.19)

3. Rooftop Lights - Indigo Parade
   [indie pop / happy]  Score: 3.01 / 7.0
     - energy close to target (+1.22)
     - acousticness close to target (+0.40)
     - valence close to target (+0.46)
     - danceability close to target (+0.46)
     - tempo_bpm close to target (+0.48)

4. Gym Hero - Max Pulse
   [pop / intense]  Score: 2.98 / 7.0
     - energy close to target (+1.47)
     - acousticness close to target (+0.10)
     - valence close to target (+0.43)
     - danceability close to target (+0.49)
     - tempo_bpm close to target (+0.48)

5. Sunrise City - Neon Echo
   [pop / happy]  Score: 2.90 / 7.0
     - energy close to target (+1.30)
     - acousticness close to target (+0.23)
     - valence close to target (+0.47)
     - danceability close to target (+0.45)
     - tempo_bpm close to target (+0.45)
```

The two label matches split the vote: Neon Pulse wins on mood plus energy, but Sonata for Rain (energy 0.22, a quiet piano piece) is a close second at 3.97 vs. 4.05 on the 2.0 genre bonus and acousticness alone. A user asking for energy 0.95 gets a slow, melancholic song at #2.

### Adversarial 3: dead center (every target 0.5, no label match)

```
Top 5 for profile: ADVERSARIAL: dead center (every target 0.5, no genre/mood fit)

1. Velvet Hours - Sable Monroe
   [r&b / romantic]  Score: 3.58 / 7.0
     - energy close to target (+1.47)
     - acousticness close to target (+0.88)
     - valence close to target (+0.40)
     - danceability close to target (+0.39)
     - tempo_bpm close to target (+0.44)

2. Dust Road Home - Willow Creek
   [country / nostalgic]  Score: 3.55 / 7.0
     - energy close to target (+1.42)
     - acousticness close to target (+0.76)
     - valence close to target (+0.41)
     - danceability close to target (+0.47)
     - tempo_bpm close to target (+0.49)

3. Midnight Coding - LoRoom
   [lofi / chill]  Score: 3.47 / 7.0
     - energy close to target (+1.38)
     - acousticness close to target (+0.79)
     - valence close to target (+0.47)
     - danceability close to target (+0.44)
     - tempo_bpm close to target (+0.39)

4. Salt & Sun - Costa Brava Collective
   [reggae / uplifting]  Score: 3.39 / 7.0
     - energy close to target (+1.35)
     - acousticness close to target (+0.95)
     - valence close to target (+0.33)
     - danceability close to target (+0.35)
     - tempo_bpm close to target (+0.41)

5. Focus Flow - LoRoom
   [lofi / focused]  Score: 3.38 / 7.0
     - energy close to target (+1.35)
     - acousticness close to target (+0.72)
     - valence close to target (+0.46)
     - danceability close to target (+0.45)
     - tempo_bpm close to target (+0.40)
```

The whole top 5 spans only 0.20 points (3.58 to 3.38) and is driven by energy and acousticness alone, so the order is close to arbitrary. A tiny change in one target would reshuffle it.

### What the stress test showed

- **Labels can dominate or vanish.** A genre match is worth 2.0, which can lift a song that is wrong in sound (Sonata for Rain at energy 0.95). If a label isn't in the catalog, it contributes nothing, and the system gives no warning that nothing matched.
- **Energy and acousticness carry most of the numeric score**, so conflicting targets between them produce a compromise that satisfies neither.
- **Scores don't signal confidence.** A 2.93 result is displayed the same way as a 6.96 result.
- **No partial credit** for near labels (metal vs. rock, melancholic vs. sad).

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.
Weakness I wrote up: the exact-match genre bonus helps some listeners much more than others.

Uneven catalog: 13 of the 15 genres have exactly one song, and lofi has three.
Who benefits: a lofi fan gets three songs earning the +2.0 genre bonus, and they fill the top three. A rock, jazz or folk fan gets that bonus on one song, and the other four slots are filled by numeric closeness alone.
No credit for near genres: indie pop Rooftop Lights lost to the intense pop song Gym Hero for pop / happy. Metal's Iron Requiem also ranks below a pop song for the rock profile.
Filter bubble: a lofi fan is mostly shown more lofi.
Energy gap: I checked whether the energy gap treats some users unfairly, and it mostly doesn't. Songs within 0.15 of the target range from 4 (energy 0.2 or 0.97) to 7 (0.9). The one oddity is that no song has energy between 0.60 and 0.75. The paragraph says this in a single closing sentence.
---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


I was originally confused on how the instructions work, and my bias for music apps that them only recommand ceritan songs that match some boxes than what the user want usually. So see the code I can see for a generic recommendation I was right, but I also it can be fix if the weights are more controlled.
