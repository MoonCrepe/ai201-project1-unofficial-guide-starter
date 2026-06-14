# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain
I chose an unofficial Animal Crossing: New Horizons gameplay guide which is supposed to help players search all kinds of informations about island life. creature collecting, flower breeding, villager interactions, and DLC access. I believe that this is useful because of just how manysmall systems with different rles, times, seasons,basically overally environmental setup along with unlock requirements there are to the game which could make it frustrating at one point for players to figure out especially if they're speedrunning the game first time. Additionally, it is difficult to find these types of informations quickly as they're spread across different guide pages, articles, or youtube videos.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Full ACNH island life guide | Broad guide covering island life, tools, crafting, collecting, characters, events, and progression.  |  https://www.gamesradar.com/animal-crossing-new-horizons-guide/|
| 2 |Fish guide | Guide to fish availability by hemisphere, month, time, and location.  |  https://www.gamesradar.com/animal-crossing-new-horizons-fish/|
| 3 |Bug guide  | Guide to bug availability by hemisphere, season, time, and location. | https://www.gamesradar.com/animal-crossing-new-horizons-bugs/|
| 4 |Sea creatures guide |Guide to diving and sea creature availability by season and time. | https://www.gamesradar.com/animal-crossing-new-horizons-sea-creatures/|
| 5 | Hybrid flowers guide|  Explanation on flower types, hybrid flower breeding, watering, and planting patterns.|  https://www.gamesradar.com/animal-crossing-new-horizons-flowers-hybrid-breeding/|
| 6 |Ordinances guide |Explanation on island ordinances, costs, effects, and how to choose one. | https://www.gamesradar.com/animal-crossing-new-horizons-ordinances-guide/|
| 7 | Villager visits and invites guide  | Explanation on villager house visits, invitations, and friendship related interactions.  |  https://www.gamesradar.com/animal-crossing-new-horizons-villager-visits-invites/|
| 8 | Happy Home Paradise access guide| Explanations on how to access the Happy Home Paradise DLC and start vacation home design work. | https://www.gamesradar.com/how-to-access-animal-crossing-new-horizons-happy-home-paradise-dlc/|
| 9 |  Wired ACNH tips| List of practical gameplay tips for inventory, resources, money, visitors, and daily play. | https://www.wired.com/story/animal-crossing-new-horizons-tips|
| 10 | ACNH gameplay overview | Overview of the game’s systems, progression, crafting, island rating, multiplayer, and updates. Basically a summary of everything important in the game. |https://en.wikipedia.org/wiki/Animal_Crossing%3A_New_Horizons |


After skimming the sources, I noticed that the sources have mixed structure in which the sources were written in defferent formats. The fish, bug, and sea creature guides are table heavy and contain many small facts about season, time, and location. In contrast, the ordinances, villager visits, DLC, and tips pages are more paragraph based. Because of this, the chunking strategy needs to preserve complete rows or short sections instead of splitting blindly every fixed number of characters.
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**  Roughly 900 characters per chunk

**Overlap:** Around 150 characters

**Reasoning:** Fow how I will split my documents into chunls. I will start splitting each cleaned document by paragraphs first. Then I will group near paragraphs together until the chunk is roughly 900 characters. If it is long, I will then split it by sentences so that the chunk doesn't become too big and subsequently, I will use around 150 characters of overlap between chunks so that importantdetailys near the end are made to be repeated in the next chunk as well. In general to explain more about the numbers, my sources include both a fact heavy guide section and a paragraph based section, So, a 900 character chunk should be large enough to keep all of the revelvant information such as time, season, and location together. The 150 character overlap will help to prevent important details from being lsot when sections are split across two chunks which is a problem as I don't want chunks that are too small as a row may not contain enough contect for semantic searches. Additionally, I don't want chunks that are too big as it could mix up unrelated topics like fish locations and flower breeding.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 utilizing a sentece transformer

**Top-k:** 4 chunks per query

**Production tradeoff reflection:** I chose this model because it could run locally, fast enought for class, and most of all, it's free. If this were for production, however, I would have to compare it to stronger embedding models that could retrieve much more accurate results for the detailed game guide questions. Overall, I'd look into accuracy rate, speed, cost, context lenght, and whether or not the model can handle table like texts well. Additionally, sinc ethis project is going to be focused on one game and language in particular, multilingual support is not as important as retrieval quality. If this was a language app then it would be a different case of course.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which ordinance should a player use if they usually play late at night? | The Night Owl Ordinance, because it makes shops stay open later and villagers more active later in the day.|
| 2 | What conditions are needed to catch a coelacanth in Animal Crossing: New Horizons? | The coelacanth appears in the sea, is available all year and all day, and requires rainy weather. |
| 3 |  How do you create hybrid flowers? | Plant compatible flowers with space between them, commonly in a checkerboard pattern, and water them regularly so hybrids can grow in open spaces. |
| 4 |  How does a player access Happy Home Paradise after getting the DLC? | After buying/downloading the DLC and restarting the game, the player gets a call from Tom Nook, goes to the airport, meets Lottie, and chooses to go to work through Orville.  |
| 5 | What can happen when villagers visit the player’s house? | Villagers may comment on decor, give an item, play a card game, ask for a room tour, and the visit can deepen friendship. |

---

---
---

## Evaluation Results

I ran each of the 5 evaluation questions through the deployed app and compared the system's answer to my expected answer.

### 1. Which ordinance should a player use if they usually play late at night?
**System answer:** The Night Owl Ordinance is the most suitable for players who usually play late at night, as it makes villagers stay active later and keeps shops open later.
**Sources retrieved:** Ordinances guide (top 2 matches), Happy Home Paradise guide, Full ACNH island life guide
**Match to expected answer:** Correct. The system matched my expected answer almost exactly, and the top 2 retrieved chunks both came from the correct source (Ordinances guide).

### 2. What conditions are needed to catch a coelacanth?
**System answer:** To catch a coelacanth, it must be raining, and it can be found in the sea. It is available all year and all day, as long as it is raining.
**Sources retrieved:** Fish guide (top 2 matches), Bug guide (2 chunks)
**Match to expected answer:** Correct. The core conditions (sea, all year, all day, rainy weather) matched my expected answer. The top 2 chunks came from the correct source (Fish guide); the Bug guide chunks ranked lower and were not used in the answer.

### 3. How do you create hybrid flowers?
**System answer:** Plant compatible flowers near each other and water them, allowing new flowers to grow in open spaces nearby. A checkerboard pattern is often used because it leaves empty spaces for hybrids to appear. Watering increases breeding chance, and visitors watering flowers can improve odds further.
**Sources retrieved:** Hybrid flowers guide (top 2 matches, lowest distance of all questions at 0.49), Wired ACNH tips, Full ACNH island life guide
**Match to expected answer:** Correct, and more detailed than my expected answer. The system added extra accurate detail (visitors watering flowers improves odds) that wasn't in my original expected answer but is consistent with the source.

### 4. How does a player access Happy Home Paradise after getting the DLC?
**System answer:** Restart the game, get a call from Tom Nook, go to the airport, meet Lottie (who introduces the vacation home design job), then talk to Orville and choose to go to work, which sends the player to the Happy Home Paradise area.
**Sources retrieved:** Happy Home Paradise access guide (top and 3rd matches), ACNH gameplay overview, Villager visits guide
**Match to expected answer:** Correct. Matches my expected answer step-for-step (Tom Nook call → airport → Lottie → Orville → work). The top retrieved chunk came from the correct source with the lowest distance (0.59) of any non-flower question.

### 5. What can happen when villagers visit the player's house?
**System answer:** Villagers may comment on furniture/decorations, give the player an item, play a card game, or ask for a tour of different rooms.
**Sources retrieved:** Villager visits and invites guide (top 2 matches), Full ACNH island life guide, Ordinances guide
**Match to expected answer:** Mostly correct but slightly incomplete. My expected answer also mentioned that visits can deepen friendship, which the system's answer left out, even though the top source (Villager visits guide) likely covers this. This suggests the chunk containing the friendship detail either wasn't retrieved or was deprioritized.

### Summary
4 out of 5 questions were fully correct and well grounded in the right source documents, with low retrieval distances (0.49–0.94) for the top chunk in each case. Question 5 was mostly correct but omitted one detail (friendship/relationship effects) from my expected answer, possibly because that information was split into a different chunk than the one retrieved. Overall, the table-heavy sources (fish, ordinances, hybrid flowers, Happy Home Paradise) retrieved especially cleanly, supporting my chunking decision to keep related facts grouped together with overlap.

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some guide pages may include navigation text, ads, repeated headings, or unrelated links. If that text gets into the chunks, retrieval might return irrelevant results instead of the actual guide content. I will then need to inspect cleaned documents and sample chunks to make sure the text is useful and relevant.

2. Some facts may unfortunately be split across chunk boundaries, especially table-\ style information about creatures where the name, time, season, and location all need to stay together. If the chunking separates those details, the system may retrieve only part of the answer. I plan to use paragraph first chunking with overlap and inspect sample chunks before embedding them.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

![Hand-drawn pipeline diagram](images/pipeline-diagram.png)
or

Document Ingestion
(Python requests + BeautifulSoup)
        ↓
Cleaning
(remove HTML, navigation, ads, repeated whitespace)
        ↓
Chunking
(paragraph-first chunks, ~900 characters, 150 overlap)
        ↓
Embedding + Vector Store
(sentence-transformers all-MiniLM-L6-v2 + ChromaDB)
        ↓
Retrieval
(top 4 chunks by semantic similarity)
        ↓
Generation
(Groq Llama model with grounded prompt)
        ↓
Interface
(Gradio web app)


## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I plan to use ChatGPT/Codex to help write the Python script that downloads or loads my Animal Crossing guide sources, removes HTML/navigation text, and splits the cleaned text into chunks. I will give it my Domain, Documents, and Chunking Strategy sections as input. I expect it to produce functions for loading documents, cleaning text, and chunking text. I will then verify the output by printing cleaned documents and at least 5 sample chunks to check that they are readable, substantive, and not full of navigation text or broken fragments. 

**Milestone 4 — Embedding and retrieval:**  I plan to use ChatGPT/Codex to help connect the chunking output to sentence-transformers and ChromaDB. I will give it my Retrieval Approach section, especially the all-MiniLM-L6-v2 model and top-k value of 4. I expect it to produce code that embeds chunks, stores them with source metadata, and retrieves the most relevant chunks for a query. I will verify it by testing at least 3 evaluation questions and checking whether the returned chunks visibly relate to the question.

**Milestone 5 — Generation and interface:** I plan to use ChatGPT/Codex to help build the grounded response function and a simple Gradio interface. I will give it my Evaluation Plan and the requirement that answers must use only retrieved chunks and cite sources. I expect it to produce an ask function and app interface with a question input, answer output, and source output. I will verify it by asking in-scope and out-of-scope questions and checking that the system cites retrieved documents or refuses to answer when the documents do not contain enough information. 
