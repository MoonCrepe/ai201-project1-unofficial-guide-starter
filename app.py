import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

from query import retrieve

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def format_context(chunks):
    context_parts = []
    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']}]\n"
            f"URL: {chunk['url']}\n"
            f"{chunk['text']}"
        )
    return "\n\n".join(context_parts)


def generate_answer(question, chunks):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Missing GROQ_API_KEY. Add it to your .env file."

    client = Groq(api_key=api_key)
    context = format_context(chunks)

    prompt = f"""
You are answering questions about Animal Crossing: New Horizons.

Use only the retrieved context below. Do not use outside knowledge.
If the context does not contain enough information to answer, say:
"I don't have enough information in the retrieved documents to answer that."

After the answer, include a Sources section naming the source documents used.

Retrieved context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a grounded guide assistant. Answer only from provided context and cite sources.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def ask(question):
    if not question.strip():
        return "Please enter a question.", ""

    chunks = retrieve(question, top_k=4)
    answer = generate_answer(question, chunks)

    sources = []
    for chunk in chunks:
        sources.append(
            f"{chunk['source']} | distance {chunk['distance']:.4f}\n{chunk['url']}"
        )

    return answer, "\n\n".join(sources)


with gr.Blocks(title="Unofficial ACNH Guide") as demo:
    gr.Markdown("# Unofficial Animal Crossing: New Horizons Guide")
    gr.Markdown("Ask a question about the collected Animal Crossing guide documents.")

    question = gr.Textbox(label="Your question")
    ask_button = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=8)

    ask_button.click(ask, inputs=question, outputs=[answer, sources])
    question.submit(ask, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()