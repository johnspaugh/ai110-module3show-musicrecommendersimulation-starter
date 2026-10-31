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

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
