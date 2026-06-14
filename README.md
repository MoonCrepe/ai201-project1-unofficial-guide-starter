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

## AI Usage

I used AI tools throughout this project for planning, coding, and debugging help.

Planning: I used ChatGPT to brainstorm domain ideas and an initial source list, which I sorted through myself. After skimming through the sources, I wrote the domain description, source descriptions, and skim notes in planning.md.

Pipeline and app code: I used ChatGPT to help write the document ingestion, chunking, embedding, retrieval, and Gradio interface code, based on the chunking strategy and retrieval approach I specified in planning.md (900-character chunks, 150-character overlap, all-MiniLM-L6-v2 embeddings, top-4 retrieval).

Debugging: I used Claude to debug environment setup issues, including a ModuleNotFoundError for gradio and a huggingface-hub version conflict between gradio and transformers, which I resolved by installing a compatible huggingface-hub version. I also got help diagnosing a Groq API authentication error caused by an invalid API key.

Evaluation: I ran my 5 evaluation questions through the deployed app myself, then used Claude to help me organize the results in planning.md. I reviewed each system answer against my expected answer myself before finalizing the assessment.