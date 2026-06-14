# Unofficial Animal Crossing: New Horizons Guide

A RAG (Retrieval-Augmented Generation) system that answers questions about Animal Crossing: New Horizons gameplay by retrieving information from a collection of online guides and generating grounded answers with source citations.

## Project Description

This project answers practical gameplay questions — fish/bug/sea creature availability, hybrid flower breeding, island ordinances, villager interactions, and Happy Home Paradise DLC access by retrieving relevant chunks from 10 ACNH guide sources and generating an answer using a Groq-hosted LLM. Every answer cites the source documents it was grounded in.

## Architecture

Document Ingestion
(Python requests + BeautifulSoup)
        v
Cleaning
(remove HTML, navigation, ads, repeated whitespace)
        v
Chunking
(paragraph-first chunks, ~900 characters, 150 overlap)
        v
Embedding + Vector Store
(sentence-transformers all-MiniLM-L6-v2 + ChromaDB)
        v
Retrieval
(top 4 chunks by semantic similarity)
        v
Generation
(Groq Llama model with grounded prompt)
        v
Interface
(Gradio web app)

## Setup

1. Clone this repository:

git clone https://github.com/MoonCrepe/ai201-project1-unofficial-guide-starter.git
cd ai201-project1-unofficial-guide-starter

2. Create and activate a virtual environment:

python -m venv .venv

Windows: .venv\Scripts\Activate
Mac/Linux: source .venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Set up your Groq API key:

cp .env.example .env

Then open .env and add your key from console.groq.com:

GROQ_API_KEY=your_key_here

## Building the Knowledge Base

python pipeline.py

## Running the App

python app.py

Open the local URL shown in the terminal (typically http://127.0.0.1:7860) in your browser.

## Example Questions

- "Which ordinance should a player use if they usually play late at night?"
- "What conditions are needed to catch a coelacanth?"
- "How do you create hybrid flowers?"
- "How does a player access Happy Home Paradise after getting the DLC?"
- "What can happen when villagers visit the player's house?"

## Sample Chunks

### Chunk 1 — Source: Full ACNH island life guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-guide/

Animal Crossing: New Horizons is a life simulation game where the player develops a deserted island into a customized community. Early progression includes gathering materials, crafting tools, catching bugs and fish, earning bells, paying off loans, and helping Tom Nook expand the island. The game encourages daily play because different resources, visitors, shop items, creatures, and events can appear on different days.

Important beginner tasks include collecting wood, stone, weeds, fruit, bugs, and fish. Players use tools such as the axe, shovel, fishing rod, net, ladder, vaulting pole, and watering can to explore and gather resources. Crafting is important because many tools and furniture items are made from materials found around the island.

### Chunk 2 — Source: Full ACNH island life guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-guide/

ing can to explore and gather resources. Crafting is important because many tools and furniture items are made from materials found around the island.

Island development expands over time. The player starts with a tent and gradually unlocks a house, museum, shop, bridge and incline construction, resident services upgrades, terraforming, and island customization. Players can decorate outdoors, place furniture, move buildings, invite villagers, and improve the island rating.

*Note: Chunk 2 begins with an overlapping ~150-character tail from the end of Chunk 1 ("...ing can to explore and gather resources. Crafting is important because many tools and furniture items are made from materials found around the island."), demonstrating the overlap behavior described in the Chunking Strategy.*

### Chunk 3 — Source: Fish guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-fish/

Fish in Animal Crossing: New Horizons appear based on location, month, time of day, weather, and hemisphere. Players catch fish using a fishing rod near rivers, ponds, river mouths, clifftop rivers, piers, and the sea. Some fish are available all day, while others only appear during specific hours.

The coelacanth is a rare fish that appears in the sea. It is available all year and all day, but only when it is raining. Because it depends on weather instead of a short time window, players should check the sea during rainy conditions and look for a large fish shadow.

Fishing can be used to fill the museum, earn bells, complete Critterpedia entries, and participate in fishing events. Rare fish are usually more valuable, but they may require specific locations or conditions.

### Chunk 4 — Source: Fish guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-fish/

e Critterpedia entries, and participate in fishing events. Rare fish are usually more valuable, but they may require specific locations or conditions.

*Note: This chunk is a short overlap-only chunk from the end of Chunk 3, caused by a source boundary (the "Fish guide" section ends shortly after this point). This shows a known edge case in the chunking logic — when a source ends right after a chunk split, the remaining overlap text becomes its own small chunk.*

## Retrieval Test Results

### Query 1: "Which ordinance should I use if I play late at night?"

| Rank | Source | Distance |
|------|--------|----------|
| 1 | Ordinances guide | 0.8736 |
| 2 | Ordinances guide (overlap chunk) | 1.1427 |
| 3 | Happy Home Paradise access guide | 1.5676 |
| 4 | Full ACNH island life guide | 1.5846 |

**Top chunk (distance 0.8736, Ordinances guide):**

> Island ordinances let players adjust island life to better match how they play. Ordinances are managed through Isabelle at Resident Services after the feature is unlocked. They cost bells to enact and affect daily behavior on the island.
>
> The Night Owl Ordinance is useful for players who usually play late at night because it makes villagers stay active later and keeps shops open later. The Early Bird Ordinance is better for players who usually play early in the morning because villagers and shops start earlier.
>
> The Beautiful Island Ordinance helps reduce weeds and makes villagers water flowers more often. The Bell Boom Ordinance increases the amount of bells players receive from selling items, but it can also increase shop prices. Choosing an ordinance depends on the player's schedule and goals.

**Why this is relevant:** This chunk directly answers the question — it names the Night Owl Ordinance and explicitly explains why it suits late-night players (shops stay open later, villagers stay active later). The second-ranked chunk is an overlap fragment from the end of the same chunk, and the third and fourth results are lower-relevance chunks from other guides that the embedding model still considered somewhat related (likely due to shared vocabulary like "island" and "players").

---

### Query 2: "How do I catch a coelacanth?"

| Rank | Source | Distance |
|------|--------|----------|
| 1 | Fish guide | 0.9363 |
| 2 | Bug guide | 1.3760 |
| 3 | Fish guide (overlap chunk) | 1.3781 |
| 4 | Bug guide (overlap chunk) | 1.4398 |

**Top chunk (distance 0.9363, Fish guide):**

> Fish in Animal Crossing: New Horizons appear based on location, month, time of day, weather, and hemisphere. Players catch fish using a fishing rod near rivers, ponds, river mouths, clifftop rivers, piers, and the sea. Some fish are available all day, while others only appear during specific hours.
>
> The coelacanth is a rare fish that appears in the sea. It is available all year and all day, but only when it is raining. Because it depends on weather instead of a short time window, players should check the sea during rainy conditions and look for a large fish shadow.
>
> Fishing can be used to fill the museum, earn bells, complete Critterpedia entries, and participate in fishing events. Rare fish are usually more valuable, but they may require specific locations or conditions.

**Why this is relevant:** The top chunk contains the exact answer — the coelacanth's location (sea), availability (all year, all day), and condition (rainy weather). The Bug guide chunks ranked second and fourth despite not mentioning the coelacanth at all; this is likely because both guides share similar structure and vocabulary around catching creatures (location, time, season), which the embedding model picked up on as topical similarity even though the content isn't directly relevant.

---

### Query 3: "How do I create hybrid flowers?"

| Rank | Source | Distance |
|------|--------|----------|
| 1 | Hybrid flowers guide | 0.4859 |
| 2 | Hybrid flowers guide (overlap chunk) | 1.1198 |
| 3 | Full ACNH island life guide | 1.6874 |
| 4 | Wired ACNH tips | 1.6937 |

**Top chunk (distance 0.4859, Hybrid flowers guide):**

> Hybrid flowers are created by planting compatible flowers near each other and watering them so new flowers can grow in open spaces nearby. Players often plant flowers in a checkerboard pattern because it leaves empty spaces for hybrids to appear. Watering flowers increases the chance of breeding, and having visitors water flowers can improve the odds even more.
>
> Different flower species and colors can produce different hybrid colors. Basic flower types include roses, tulips, pansies, windflowers, hyacinths, mums, lilies, and cosmos. Hybrid breeding can create colors such as pink, orange, purple, blue, black, and gold depending on the species and parent colors.
>
> The key idea is that flowers need space, compatible parents, and watering. Hybrid breeding can take time because the result is chance-based. Players may need to try multiple layouts or generations of flowers to get rare hybrids.

This was the strongest retrieval result across all test queries — distance 0.4859 is roughly half the distance of the next-best result in any query, indicating very high semantic similarity between the query and the top chunk.



## How Grounded Generation Is Enforced

Grounded generation is enforced through prompt design and pipeline structure in `app.py`:

1. **Retrieval before generation:** For every question, the system first retrieves the top 4 most relevant chunks via `retrieve()` (semantic search over ChromaDB). These chunks are passed into the prompt — the model never sees the question without context.

2. **Explicit "context only" instruction:** The prompt explicitly states: *"Use only the retrieved context below. Do not use outside knowledge."* This is reinforced by the system message: *"You are a grounded guide assistant. Answer only from provided context and cite sources."*

3. **Required refusal behavior:** The prompt instructs the model that if the retrieved context doesn't contain enough information, it must respond: *"I don't have enough information in the retrieved documents to answer that."* This prevents the model from hallucinating an answer when retrieval fails to find relevant chunks.

4. **Source labeling in context:** Each retrieved chunk is formatted with `[Source N: <document name>]` and its URL before being inserted into the prompt (via `format_context()`). This gives the model explicit source labels to cite in its "Sources" section, rather than relying on it to invent or remember source names.

5. **Low temperature:** Generation uses `temperature=0.2`, reducing creative variation and keeping responses closer to the literal content of the retrieved chunks.

6. **Independent source display:** Separately from the model's own "Sources" section in its answer, the app's "Retrieved From" field independently lists the actual chunks retrieved (with source names, distances, and URLs) directly from the retrieval step — not generated by the model. This lets a user verify the model's citations against the real retrieved chunks, catching cases where the model's cited sources don't match what was actually retrieved.


## Sample Chunks

Chunk 1 - Source: Full ACNH island life guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-guide/

Animal Crossing: New Horizons is a life simulation game where the player develops a deserted island into a customized community. Early progression includes gathering materials, crafting tools, catching bugs and fish, earning bells, paying off loans, and helping Tom Nook expand the island. The game encourages daily play because different resources, visitors, shop items, creatures, and events can appear on different days.

Important beginner tasks include collecting wood, stone, weeds, fruit, bugs, and fish. Players use tools such as the axe, shovel, fishing rod, net, ladder, vaulting pole, and watering can to explore and gather resources. Crafting is important because many tools and furniture items are made from materials found around the island.

Chunk 2 - Source: Full ACNH island life guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-guide/

ing can to explore and gather resources. Crafting is important because many tools and furniture items are made from materials found around the island.

Island development expands over time. The player starts with a tent and gradually unlocks a house, museum, shop, bridge and incline construction, resident services upgrades, terraforming, and island customization. Players can decorate outdoors, place furniture, move buildings, invite villagers, and improve the island rating.

Note: Chunk 2 begins with an overlapping ~150-character tail from the end of Chunk 1, demonstrating the overlap behavior described in the Chunking Strategy.

Chunk 3 - Source: Fish guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-fish/

Fish in Animal Crossing: New Horizons appear based on location, month, time of day, weather, and hemisphere. Players catch fish using a fishing rod near rivers, ponds, river mouths, clifftop rivers, piers, and the sea. Some fish are available all day, while others only appear during specific hours.

The coelacanth is a rare fish that appears in the sea. It is available all year and all day, but only when it is raining. Because it depends on weather instead of a short time window, players should check the sea during rainy conditions and look for a large fish shadow.

Fishing can be used to fill the museum, earn bells, complete Critterpedia entries, and participate in fishing events. Rare fish are usually more valuable, but they may require specific locations or conditions.

Chunk 4 - Source: Fish guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-fish/

e Critterpedia entries, and participate in fishing events. Rare fish are usually more valuable, but they may require specific locations or conditions.

Note: This chunk is a short overlap-only chunk caused by a source boundary, since the Fish guide section ends shortly after this point. This shows a known edge case where the remaining overlap text becomes its own small chunk.

Chunk 5 - Source: Hybrid flowers guide
URL: https://www.gamesradar.com/animal-crossing-new-horizons-flowers-hybrid-breeding/

Hybrid flowers are created by planting compatible flowers near each other and watering them so new flowers can grow in open spaces nearby. Players often plant flowers in a checkerboard pattern because it leaves empty spaces for hybrids to appear. Watering flowers increases the chance of breeding, and having visitors water flowers can improve the odds even more.

Different flower species and colors can produce different hybrid colors. Basic flower types include roses, tulips, pansies, windflowers, hyacinths, mums, lilies, and cosmos. Hybrid breeding can create colors such as pink, orange, purple, blue, black, and gold depending on the species and parent colors.

The key idea is that flowers need space, compatible parents, and watering. Hybrid breeding can take time because the result is chance-based. Players may need to try multiple layouts or generations of flowers to get rare hybrids.


## Retrieval Test Results

Query 1: "Which ordinance should I use if I play late at night?"

Rank 1 - Source: Ordinances guide - Distance: 0.8736
Rank 2 - Source: Ordinances guide (overlap chunk) - Distance: 1.1427
Rank 3 - Source: Happy Home Paradise access guide - Distance: 1.5676
Rank 4 - Source: Full ACNH island life guide - Distance: 1.5846

Top chunk (distance 0.8736, Ordinances guide):

Island ordinances let players adjust island life to better match how they play. Ordinances are managed through Isabelle at Resident Services after the feature is unlocked. They cost bells to enact and affect daily behavior on the island.

The Night Owl Ordinance is useful for players who usually play late at night because it makes villagers stay active later and keeps shops open later. The Early Bird Ordinance is better for players who usually play early in the morning because villagers and shops start earlier.

The Beautiful Island Ordinance helps reduce weeds and makes villagers water flowers more often. The Bell Boom Ordinance increases the amount of bells players receive from selling items, but it can also increase shop prices. Choosing an ordinance depends on the player's schedule and goals.

Why this is relevant: This chunk directly answers the question, naming the Night Owl Ordinance and explaining why it suits late-night players. The second-ranked result is an overlap fragment from the same chunk, and the third and fourth results are lower-relevance chunks from other guides that the embedding model still considered loosely related, likely due to shared vocabulary like "island" and "players."


Query 2: "How do I catch a coelacanth?"

Rank 1 - Source: Fish guide - Distance: 0.9363
Rank 2 - Source: Bug guide - Distance: 1.3760
Rank 3 - Source: Fish guide (overlap chunk) - Distance: 1.3781
Rank 4 - Source: Bug guide (overlap chunk) - Distance: 1.4398

Top chunk (distance 0.9363, Fish guide):

Fish in Animal Crossing: New Horizons appear based on location, month, time of day, weather, and hemisphere. Players catch fish using a fishing rod near rivers, ponds, river mouths, clifftop rivers, piers, and the sea. Some fish are available all day, while others only appear during specific hours.

The coelacanth is a rare fish that appears in the sea. It is available all year and all day, but only when it is raining. Because it depends on weather instead of a short time window, players should check the sea during rainy conditions and look for a large fish shadow.

Fishing can be used to fill the museum, earn bells, complete Critterpedia entries, and participate in fishing events. Rare fish are usually more valuable, but they may require specific locations or conditions.

Why this is relevant: The top chunk contains the exact answer, including the coelacanth's location, availability, and weather condition. The Bug guide chunks ranked second and fourth despite not mentioning the coelacanth at all, likely because both guides share similar structure and vocabulary around catching creatures (location, time, season), which the embedding model picked up as topical similarity even though the content isn't directly relevant.


Query 3: "How do I create hybrid flowers?"

Rank 1 - Source: Hybrid flowers guide - Distance: 0.4859
Rank 2 - Source: Hybrid flowers guide (overlap chunk) - Distance: 1.1198
Rank 3 - Source: Full ACNH island life guide - Distance: 1.6874
Rank 4 - Source: Wired ACNH tips - Distance: 1.6937

Top chunk (distance 0.4859, Hybrid flowers guide):

Hybrid flowers are created by planting compatible flowers near each other and watering them so new flowers can grow in open spaces nearby. Players often plant flowers in a checkerboard pattern because it leaves empty spaces for hybrids to appear. Watering flowers increases the chance of breeding, and having visitors water flowers can improve the odds even more.

Different flower species and colors can produce different hybrid colors. Basic flower types include roses, tulips, pansies, windflowers, hyacinths, mums, lilies, and cosmos. Hybrid breeding can create colors such as pink, orange, purple, blue, black, and gold depending on the species and parent colors.

The key idea is that flowers need space, compatible parents, and watering. Hybrid breeding can take time because the result is chance-based. Players may need to try multiple layouts or generations of flowers to get rare hybrids.

This was the strongest retrieval result across all test queries. A distance of 0.4859 is roughly half the distance of the next-best result in any query, indicating very high semantic similarity between the query and the top chunk.


## How Grounded Generation Is Enforced

Grounded generation is enforced through prompt design and pipeline structure in app.py:

1. Retrieval before generation: For every question, the system first retrieves the top 4 most relevant chunks via retrieve(), which performs semantic search over ChromaDB. These chunks are passed into the prompt, so the model never sees the question without context.

2. Explicit "context only" instruction: The prompt explicitly states that the model should use only the retrieved context and not outside knowledge. This is reinforced by the system message, which tells the model it is a grounded guide assistant that should answer only from provided context and cite sources.

3. Required refusal behavior: The prompt instructs the model that if the retrieved context does not contain enough information, it must respond with a specific refusal message. This prevents the model from hallucinating an answer when retrieval fails to find relevant chunks.

4. Source labeling in context: Each retrieved chunk is formatted with a source label and URL before being inserted into the prompt, via format_context(). This gives the model explicit source labels to cite, rather than relying on it to invent or remember source names.

5. Low temperature: Generation uses a temperature of 0.2, reducing creative variation and keeping responses closer to the literal content of the retrieved chunks.

6. Independent source display: Separately from the model's own Sources section in its answer, the app's Retrieved From field independently lists the actual chunks retrieved, including source names, distances, and URLs, directly from the retrieval step rather than from the model. This lets a user verify the model's citations against the real retrieved chunks, catching cases where the model's cited sources don't match what was actually retrieved.


## Example Responses

Example 1: In-scope query with source attribution

Question: "Which ordinance should a player use if they usually play late at night?"

Answer: The Night Owl Ordinance is the most suitable for players who usually play late at night, as it makes villagers stay active later and keeps shops open later.

Sources: Source 1: Ordinances guide - https://www.gamesradar.com/animal-crossing-new-horizons-ordinances-guide/

Retrieved From: SOURCE 6: Ordinances guide | distance 0.8736 - https://www.gamesradar.com/animal-crossing-new-horizons-ordinances-guide/


Example 2: In-scope query with source attribution

Question: "How do you create hybrid flowers?"

Answer: To create hybrid flowers in Animal Crossing: New Horizons, you need to plant compatible flowers near each other and water them, allowing new flowers to grow in open spaces nearby. A checkerboard pattern is often used because it leaves empty spaces for hybrids to appear. Watering flowers increases the chance of breeding, and having visitors water flowers can improve the odds even more.

Sources: Source 1: Hybrid flowers guide - https://www.gamesradar.com/animal-crossing-new-horizons-flowers-hybrid-breeding/

Retrieved From: SOURCE 5: Hybrid flowers guide | distance 0.4859 - https://www.gamesradar.com/animal-crossing-new-horizons-flowers-hybrid-breeding/


Example 3: Out-of-scope query (refusal)

Question: "What is the weather like in Pokemon Scarlet and Violet?"

Answer: I don't have enough information in the retrieved documents to answer that.

Sources: None of the provided source documents (Hybrid flowers guide, Bug guide, Sea creatures guide, Ordinances guide) contain information about Pokemon Scarlet and Violet or their weather.

Retrieved From: SOURCE 5: Hybrid flowers guide | distance 1.4015 - https://www.gamesradar.com/animal-crossing-new-horizons-flowers-hybrid-breeding/ (and additional sources with similarly high distances)

This example demonstrates the grounding mechanism working correctly. Even though retrieval still returned its top-4 closest chunks, the high distance values (1.4+) compared to the in-scope examples (0.49-0.87) indicate weak relevance. The model correctly recognized that none of the retrieved content was relevant and refused to answer rather than hallucinating information about a different game.


## Query Interface

The application is a Gradio web interface with the following fields:

**Input:**
- **Your question** (textbox) — the user types a natural-language question about Animal Crossing: New Horizons. Pressing Enter or clicking "Ask" submits the question.

**Outputs:**
- **Answer** (textbox, 10 lines) — displays the model's generated response, including its own "Sources" section citing which documents it used.
- **Retrieved from** (textbox, 8 lines) — independently displays the actual chunks retrieved by the vector search, showing each chunk's source document, similarity distance, and URL.

### Sample Interaction Transcript

**User input:** "How does a player access Happy Home Paradise after getting the DLC?"

**Answer field:**
> To access Happy Home Paradise after getting the DLC, the player needs to restart the game. After the game is restarted, Tom Nook will call the player and ask them to come to the airport. At the airport, the player will meet Lottie, who will introduce the vacation home design job. The player can then talk to Orville and choose the option to go to work, which will send them to the Happy Home Paradise island area where they can design vacation homes for clients.
>
> Sources:
> [Source 1: Happy Home Paradise access guide] https://www.gamesradar.com/how-to-access-animal-crossing-new-horizons-happy-home-paradise-dlc/

**Retrieved from field:**
```
SOURCE 8: Happy Home Paradise access guide | distance 0.5941
https://www.gamesradar.com/how-to-access-animal-crossing-new-horizons-happy-home-paradise-dlc/

SOURCE 10: ACNH gameplay overview | distance 1.1818
https://en.wikipedia.org/wiki/Animal_Crossing%3A_New_Horizons

SOURCE 8: Happy Home Paradise access guide | distance 1.2533
https://www.gamesradar.com/how-to-access-animal-crossing-new-horizons-happy-home-paradise-dlc/

SOURCE 7: Villager visits and invites guide | distance 1.4222
https://www.gamesradar.com/animal-crossing-new-horizons-villager-visits-invites/
```

## Spec Reflection

**How the spec helped:** Writing out the Chunking Strategy section in planning.md before implementation forced me to think through the tradeoff between chunk size and content type ahead of time. Because I noted that my sources mix table-heavy guides (fish, bugs, sea creatures) with paragraph-based guides (ordinances, DLC, tips), I specified a chunk size (900 characters) and overlap (150 characters) large enough to keep related facts together. When I tested retrieval later, this paid off — for example, the top chunk for "How do I catch a coelacanth?" contained the fish's location, season, time, and weather condition all in one chunk, which wouldn't have been possible with a much smaller chunk size.

**Where implementation diverged from the spec:** My original AI Tool Plan only described using ChatGPT/Codex for Milestones 3-5 (ingestion/chunking, embedding/retrieval, and generation/interface). In practice, I also relied heavily on Claude for debugging environment and dependency issues that came up after the initial code was generated — including a missing gradio module, a huggingface-hub version conflict between gradio and transformers, and a Groq API authentication error from an invalid key. The original plan didn't anticipate that environment setup and dependency management would require their own debugging pass separate from the pipeline code itself.

## Honest Failure Case

**Question:** "What can happen when villagers visit the player's house?"

**Expected answer (from planning.md):** Villagers may comment on decor, give an item, play a card game, ask for a room tour, and the visit can deepen friendship.

**System's actual answer:** Villagers may comment on the player's furniture and decorations, give the player an item, play a card game, or ask for a tour of different rooms.

**What went wrong:** The system's answer covered 4 out of 5 points in my expected answer but omitted that visits can deepen friendship with the villager. The top retrieved chunk (Villager visits and invites guide, distance 0.6441) was clearly the correct source document, so retrieval worked — but the specific sentence about friendship was likely located in a different chunk of the same source document that wasn't among the top-4 retrieved chunks.

**Why this happened:** This is a chunk-boundary issue. My chunking strategy groups paragraphs together up to ~900 characters, but a single source document can span many chunks. If the "friendship" detail was in a chunk further from the query's semantic center (e.g., mentioned briefly at the end of a longer section about something else), it would rank lower in similarity even though it's part of the same source and topic. A higher top-k (e.g., top-6 instead of top-4) might have retrieved this chunk as well, at the cost of including more potentially irrelevant content in the prompt.



## AI Usage

I used AI tools throughout this project for planning, coding, and debugging help.

Planning: I used ChatGPT to brainstorm domain ideas and an initial source list, which I sorted through myself. After skimming through the sources, I wrote the domain description, source descriptions, and skim notes in planning.md.

Pipeline and app code: I used ChatGPT to help write the document ingestion, chunking, embedding, retrieval, and Gradio interface code, based on the chunking strategy and retrieval approach I specified in planning.md (900-character chunks, 150-character overlap, all-MiniLM-L6-v2 embeddings, top-4 retrieval).

Debugging: I used Claude to debug environment setup issues, including a ModuleNotFoundError for gradio and a huggingface-hub version conflict between gradio and transformers, which I resolved by installing a compatible huggingface-hub version. I also got help diagnosing a Groq API authentication error caused by an invalid API key.

Evaluation: I ran my 5 evaluation questions through the deployed app myself, then used Claude to help me organize the results in planning.md. I reviewed each system answer against my expected answer myself before finalizing the assessment.