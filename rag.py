import numpy as np
from pypdf import PdfReader

EMBEDDING_MODEL = "text-embedding-3-small"

def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages).strip()

def split_text(text: str, chunk_size: int = 900, overlap: int = 150):
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

def embed_texts(client, texts):
    vectors = []
    batch_size = 64
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        vectors.extend([item.embedding for item in response.data])
    return np.array(vectors, dtype=np.float32)

def retrieve_context(client, query, chunks, vectors, top_k: int = 4):
    query_vector = embed_texts(client, [query])[0]
    matrix = np.asarray(vectors, dtype=np.float32)
    q_norm = np.linalg.norm(query_vector) + 1e-10
    d_norms = np.linalg.norm(matrix, axis=1) + 1e-10
    scores = matrix @ query_vector / (d_norms * q_norm)
    best_indices = np.argsort(scores)[::-1][:top_k]
    return "\n\n".join(
        f"[Section {idx + 1} | similarity {scores[idx]:.3f}]\n{chunks[idx]}"
        for idx in best_indices
    )
