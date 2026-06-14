import re
from pathlib import Path

DOCUMENT_PATH = Path("documents/acnh_sources.txt")
CHUNK_SIZE = 900
OVERLAP = 150


def load_document(path=DOCUMENT_PATH):
    text = path.read_text(encoding="utf-8")
    return text


def clean_text(text):
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_sources(text):
    parts = re.split(r"\n(?=SOURCE \d+:)", text)
    sources = []

    intro = parts[0].strip()
    for part in parts[1:]:
        lines = part.strip().splitlines()
        title = lines[0].strip()
        url = ""
        body_lines = []

        for line in lines[1:]:
            if line.startswith("URL:"):
                url = line.replace("URL:", "").strip()
            else:
                body_lines.append(line)

        sources.append(
            {
                "title": title,
                "url": url,
                "text": clean_text("\n".join(body_lines)),
            }
        )

    return sources


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        else:
            sentences = [paragraph]

        for unit in sentences:
            if not current:
                current = unit
            elif len(current) + len(unit) + 2 <= chunk_size:
                current += "\n\n" + unit
            else:
                chunks.append(current.strip())
                overlap_text = current[-overlap:] if overlap > 0 else ""
                current = (overlap_text + "\n\n" + unit).strip()

    if current:
        chunks.append(current.strip())

    return chunks


def build_chunks():
    raw_text = load_document()
    clean = clean_text(raw_text)
    sources = split_sources(clean)

    all_chunks = []
    for source in sources:
        chunks = chunk_text(source["text"])
        for index, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "id": f"{source['title'].lower().replace(' ', '-')}-{index}",
                    "text": chunk,
                    "source": source["title"],
                    "url": source["url"],
                    "chunk_index": index,
                }
            )

    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Loaded {len(chunks)} chunks.\n")

    for chunk in chunks[:5]:
        print("=" * 80)
        print(f"Source: {chunk['source']}")
        print(f"URL: {chunk['url']}")
        print(chunk["text"])
        print()