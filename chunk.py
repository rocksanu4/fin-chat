import re
import json

def chunk_text(text, max_chunk_size=500):
    # Split on double newlines (paragraphs), fallback to sentence boundaries
    paragraphs = re.split(r'\n{2,}', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current_chunk) + len(para) <= max_chunk_size:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

with open("reliance_raw_text.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()


text_chunks = chunk_text(raw_text)

chunks_with_meta = [
    {"text": chunk, "source": "reliance_ar2024", "type": "financial_statement"}
    for chunk in text_chunks
]

with open("chunks.json", "w", encoding="utf-8") as w:
    json.dump(chunks_with_meta, w, indent=2)

