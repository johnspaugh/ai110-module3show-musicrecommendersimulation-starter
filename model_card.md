# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

I think "songs recommend to users" would be good name descripting the ablities

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

It takes a users profile and uses as the base and assume the user will like similar songs
Then it will take that to recommand similar songs in its database, so I think it be for user not classrooms.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The recommender works like a judge at a talent show who scores every song in the catalog, one at a time, and then reads out the top five.

**What the judge looks at.** Each song has a genre (like lofi or rock), a mood (like chill or intense), and five numbers that describe how it sounds: energy, how acoustic it is, how happy it sounds (valence), how danceable it is, and its speed in beats per minute.

**What the listener tells us.** A listener has one favorite genre, one favorite mood, and a target for each of the five numbers. For example, a lofi fan might want low energy, a very acoustic sound and a slow tempo.

**How a song earns points.** Each song can earn up to 7 points:
- 2 points if its genre is the listener's favorite.
- 1 point if its mood is the listener's favorite.
- Up to 4 more points for how close its numbers are to the listener's targets. The closer, the more points. A song that is too energetic loses points just like one that is too sleepy. Energy counts the most (up to 1.5), acousticness next (up to 1.0), and valence, danceability and tempo are small tie-breakers (0.5 each).

Genre is worth more than mood because it is the more stable part of someone's taste, while mood changes by the hour. Labels alone are at most 3 of the 7 points, so a song cannot win just by having the right tag. Its sound has to fit too.

**Picking the winners.** Once every song has a score, the program sorts them from highest to lowest and shows the top five. Next to each song it lists exactly which rules gave it points, for example "genre match (+2.0)" or "energy close to target (+1.47)", so the listener can see why it was chosen.

**What changed from the starter code.** The starter only had empty placeholders. I added the CSV loader, the point-based scoring, the ranking step, and a command-line display that prints the scores and reasons. This is a "CLI-first" simulation: everything runs in the terminal, with no web page or app.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  
Profile	What happened
Deep intense rock	Works as intended. Storm Runner scores 6.96 / 7.0. Iron Requiem (metal, angry) fits musically but gets no label points because it isn't "rock" or "intense".
Sad but high energy (blues / sad, energy 0.90)	Neither label exists in the catalog, so the best score is only 2.93. The top 5 are quiet acoustic songs (energy 0.33–0.55) for a user who asked for energy 0.90. Iron Requiem and Sonata for Rain, which better fit "sad and intense", don't appear.
Classical at the gym	Neon Pulse wins with 4.05, but Sonata for Rain, a quiet piano piece with energy 0.22, is a close second at 3.97 on the genre bonus and acousticness alone.
Dead center (every target 0.5)	The top 5 span only 0.20 points, so the order is close to arbitrary.
What the stress test showed

Labels: a genre match (2.0 points) can lift a song that sounds wrong. A label that isn't in the catalog contributes nothing, and nothing warns the user.
Conflicting targets: energy and acousticness carry most of the numeric score. When the targets conflict, the result is a compromise that satisfies neither.
Confidence: a 2.93 result is displayed the same way as a 6.96 result.
Near labels: there is no partial credit, for example metal vs. rock or melancholic vs. sad.
Running main.py now prints all six profiles, so the output is long. I can add a way to pick one profile from the command line if you'd like.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  
I ran the weight shift (genre 2.0 → 1.0, energy 1.5 → 3.0) as a temporary override. recommender.py is unchanged and still has the original weights. Nothing was committed.

Math check: the maximum score becomes 1.0 + 1.0 + 3.0 + 1.0 + 1.5 = 7.5, up from 7.0. Across all 6 profiles × 18 songs, scores ran from 1.85 to 7.44, so none fell outside 0–7.5. The / 7.0 in the main.py display would be wrong under these weights and would need updating if you kept them.

Effect on the rankings

Profile	Result	Better, or just different?
pop / happy	Rooftop Lights moves above Gym Hero	Better. This was the surprise I flagged last step. A happy listener now gets the happy song first.
lofi / chill	No change	Neither. Labels and sound already agreed.
deep intense rock	Top 4 unchanged; #5 swaps Night Drive Loop for Sunrise City	Worse. Sunrise City (pop, happy) is a cheerful song in a "deep intense" list, and it only gets there on energy.
sad but high energy	Completely different list	Mixed. It now follows the energy 0.90 request (Storm Runner, Night Drive Loop, Iron Requiem, Concrete Crown), but it ignores the sad / acoustic half of the profile, so it's a different compromise and not a clearly better one.
classical at the gym	Sonata for Rain drops out; Storm Runner enters	Better. A quiet piano piece no longer ranks second for an energy 0.95 request.
dead center	No change	Neither. No labels and every target is 0.5, so nothing moves.
The change makes the system follow numbers over labels. That helps when labels are misleading (Gym Hero, Sonata for Rain) and hurts when the label carries the intent (Sunrise City in the rock list). It makes the results different, and more accurate in three of the six profiles.

Caveats: this is on 18 made-up songs and 6 profiles. The "better" calls are my own judgment of what each listener would want, not a measured metric.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness found: the genre bonus helps some listeners far more than others.** Of the 15 genres in the 18-song catalog, 13 have exactly one song, while lofi has three. A lofi fan gets three songs that earn the +2.0 genre bonus and sees them fill the top three, but a rock, jazz or folk fan gets that bonus on a single song, and the other four slots are filled purely on how close the numbers are. Because genre only matches exactly, near neighbors get nothing: in the pop / happy test, "indie pop" Rooftop Lights lost to the intense pop song Gym Hero because it earned no genre credit, and the rock profile ranks metal's Iron Requiem below a pop song. The system therefore works best for users whose favorite genre happens to be well represented, and this is a filter-bubble risk, since a lofi fan is mostly shown more lofi. The energy gap itself is fairly even, apart from a gap in the catalog with no songs between energy 0.60 and 0.75.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles I tested

I ran six listener profiles against the 18-song catalog and looked at the top five for each. Full terminal output is in the README.

| Label | Profile | Top 5 |
|---|---|---|
| A | Happy pop (pop, happy, energetic) | Sunrise City, Gym Hero, Rooftop Lights, Night Drive Loop, Concrete Crown |
| B | Chill lofi (lofi, chill, quiet, acoustic) | Midnight Coding, Library Rain, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories |
| C | Deep intense rock (rock, intense, very loud) | Storm Runner, Gym Hero, Iron Requiem, Neon Pulse, Night Drive Loop |
| D | Trick profile: sad but high energy (blues, sad, wants loud and acoustic) | Hollow Porch, Dust Road Home, Library Rain, Focus Flow, Coffee Shop Stories |
| E | Trick profile: classical at the gym (classical, euphoric, wants loud and acoustic) | Neon Pulse, Sonata for Rain, Rooftop Lights, Gym Hero, Sunrise City |
| F | Trick profile: dead center (no genre or mood, everything medium) | Velvet Hours, Dust Road Home, Midnight Coding, Salt & Sun, Focus Flow |

A, B and C are normal listeners, and I checked each result against my own sense of what that listener would want. D, E and F are trick profiles built to confuse the scoring. I also ran one experiment where I halved the genre weight and doubled the energy weight, then compared the lists.

### What surprised me

- **Gym Hero keeps showing up.** It is second for the happy pop listener, second for the rock listener, and fourth for the classical-at-the-gym listener. See the plain-language explanation below.
- **The sad, high-energy listener got quiet songs.** They asked for energy 0.90 and got songs with energy 0.33 to 0.55, because the system also saw "very acoustic" and gave that nearly as much weight.
- **A label that does not exist counts for nothing.** Nobody has the genre "blues" or the mood "sad", so profile D's best score was only 2.93 out of 7, but the list is displayed with the same confidence as a good match.
- **The messy middle profile still returned a clean-looking list.** Profile F's five songs are separated by only 0.20 points, so their order is close to arbitrary.

### Why Gym Hero keeps showing up for people who just want "Happy Pop"

Think of the system as a judge handing out points. A song gets 2 points if its genre is exactly the listener's favorite, 1 point if its mood matches, and up to 4 more points for sounding close to what the listener asked for, mostly in energy. Gym Hero is a pop song, so a "happy pop" listener gives it the 2 genre points straight away, even though its mood is "intense", not "happy". It also has very high energy, which a lively pop listener wants, so it collects most of the sound points too. Rooftop Lights is actually a closer musical fit, since it is happy and upbeat, but it is labeled "indie pop", and the system only counts an exact genre match, so it gets no genre points. The mood point is worth only half as much as the genre point, so Gym Hero wins by about 0.8 points. When I turned the genre weight down, Rooftop Lights moved above Gym Hero, which is what a happy pop listener probably wants. Gym Hero also appears for the rock listener, because "intense" matches its mood and its energy is nearly perfect. It is a song that sits in the overlap between pop and rock, so it shows up for both.

### Comparing each pair of profiles

- **A vs. B (happy pop vs. chill lofi):** no songs in common. A gets bright, energetic, danceable songs, and B gets slow, quiet, acoustic ones. This is what the profiles should test for, and the output is right.
- **A vs. C (happy pop vs. intense rock):** they share Gym Hero and Night Drive Loop, because both listeners want high energy. Past that, A gets happy songs and C gets harsh, loud ones, which is correct.
- **A vs. D (happy pop vs. sad, high energy):** no overlap. D wants low valence (a dark sound) and heavy acoustics, so it moves away from A's cheerful, electronic songs, as it should.
- **A vs. E (happy pop vs. classical at the gym):** they share three songs (Sunrise City, Rooftop Lights, Gym Hero), because E asked for high energy, happiness and danceability, which is the same thing A wants. This makes sense, but it also shows E's "classical" label did little against the numbers.
- **A vs. F (happy pop vs. dead center):** no overlap. F has no labels to match, so it picks songs near the middle on every feature (r&b, country, lofi), while A reaches for the extreme-energy, high-mood pop songs. This is right.
- **B vs. C (chill lofi vs. intense rock):** no overlap, and they are almost opposites in energy (about 0.4 vs. 0.9) and acousticness. This is the clearest sign the system can tell "intense" from "chill".
- **B vs. D (chill lofi vs. sad, high energy):** they share Library Rain, Focus Flow and Coffee Shop Stories. This is a problem. D asked for energy 0.90, but the acoustic request dragged it into B's quiet territory. The output does not match what D wanted, and it is the weakest result I found.
- **B vs. E (chill lofi vs. classical at the gym):** no overlap. E wanted loud and euphoric, and B wanted quiet and chill, so they separate cleanly.
- **B vs. F (chill lofi vs. dead center):** they share Midnight Coding and Focus Flow. Lofi sits close to the middle on most features, so a listener with no strong preference lands near lofi, which makes sense.
- **C vs. D (intense rock vs. sad, high energy):** no overlap. Both asked for high energy, but D's acoustic and low-valence request pulled it to quiet folk and country, while C got loud rock and metal. This shows that when two targets conflict, acousticness can outweigh energy.
- **C vs. E (intense rock vs. classical at the gym):** they share only Neon Pulse. Both want high energy, but E's euphoric, danceable targets pushed it toward edm and happy pop, and C's dark, harsh targets kept it near rock and metal, which is what each profile asked for.
- **C vs. F (intense rock vs. dead center):** no overlap. C picks the loudest songs and F picks medium ones, so the system responds correctly to a very high target and a middle target.
- **D vs. E (the two conflicted profiles):** no overlap. Both mix "loud" with "acoustic," but D had no matching labels and slid toward quiet songs, while E had a mood match (euphoric) and a genre match (classical) that split its top two. The way a conflicted profile resolves depends on whether any label is in the catalog.
- **D vs. F (sad, high energy vs. dead center):** they share only Dust Road Home. D has an acoustic lean and F is medium on everything, so both end up with moderate-energy acoustic-ish songs. It makes sense, but it shows D's "high energy" request is not doing much work.
- **E vs. F (classical at the gym vs. dead center):** no overlap. E wants very high energy and happy, danceable songs, and F wants medium everything, so they separate as expected.

**Overall:** for the three normal profiles (A, B, C) the results matched my intuition, apart from Gym Hero's position for A. The trick profiles showed where the system breaks: unmatched labels contribute nothing, acousticness can override energy, and middle-of-the-road profiles get nearly arbitrary rankings.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

for possible future work would be expand my database of songs, then I can do more testing
and debugging to see if the collect of more than 5 songs is being done for all the generas.
Then maybe refine the points given to each generas to reflect the user's preferenece more.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I confused by the first steps because it didn't actual need to do any coding, it just need me to plan and see how the AI assistent would act when prompt some planing questions. Once I figured that out, I went through and and continued the question to AI assistent in order to create most of the code. It seem to work okay, and see how the recommndation code operates is interesting and if I could adjust the weight values myself I think I could make better use of music apps. 

