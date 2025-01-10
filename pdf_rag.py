import os
import re
import json
import PyPDF2
import faiss
from openai import OpenAI

client = OpenAI()
import numpy as np
import pytesseract
import tiktoken
from pdf2image import convert_from_path
from PIL import Image

###############################################################################
#                           PDF CHUNKING FUNCTIONS
###############################################################################

def tokenize_and_chunk(text, chunk_size=500, model="cl100k_base"):
    """
    Tokenize and split text into chunks based on the token limit, avoiding sentence splitting.
    """
    encoding = tiktoken.get_encoding(model)
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        current_chunk_tokens = len(encoding.encode(current_chunk))
        sentence_tokens = len(encoding.encode(sentence))

        if current_chunk_tokens + sentence_tokens > chunk_size:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += (" " + sentence if current_chunk else sentence)

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def process_pdf_for_rag(pdf_path, ocr_language="eng", poppler_path=None, chunk_size=500):
    """
    Process a PDF for RAG by extracting text, images (OCR), and then chunking.
    """
    extracted_text_list = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_idx, page in enumerate(reader.pages, start=1):
            raw_text = page.extract_text()
            if raw_text:
                extracted_text_list.append(raw_text)

    # Convert PDF pages to images for OCR
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    for i, image in enumerate(images, start=1):
        ocr_text = pytesseract.image_to_string(image, lang=ocr_language)
        if ocr_text.strip():
            extracted_text_list.append(f"[Image {i} OCR]\n{ocr_text}")

    combined_text = "\n".join(extracted_text_list)

    # Tokenize/Chunk
    chunks = tokenize_and_chunk(combined_text, chunk_size=chunk_size)
    print(f"[INFO] Processed PDF -> {len(chunks)} total chunks.")
    return chunks


###############################################################################
#                       OPENAI EMBEDDING + FAISS FUNCTIONS
###############################################################################

def embed_chunks_openai(chunks, model="text-embedding-ada-002", batch_size=20):
    """
    Embed a list of text chunks using OpenAI embeddings.
    """
    print(f"[INFO] Embedding {len(chunks)} chunks with OpenAI model '{model}'...")
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        response = client.embeddings.create(input=batch, model=model)
        for r in response.data:
            embeddings.append(r["embedding"])
    embeddings = np.array(embeddings, dtype=np.float32)
    print(f"[INFO] Finished embedding. Shape: {embeddings.shape}")
    return embeddings


def create_faiss_index(embeddings):
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)
    print(f"[INFO] FAISS index created with {index.ntotal} vectors.")
    return index


def save_faiss_index(index, index_path):
    faiss.write_index(index, index_path)
    print(f"[INFO] FAISS index saved to {index_path}")


def load_faiss_index(index_path):
    if not os.path.isfile(index_path):
        raise FileNotFoundError(f"{index_path} not found.")
    index = faiss.read_index(index_path)
    print(f"[INFO] Loaded FAISS index from {index_path}, with {index.ntotal} vectors.")
    return index


def save_embeddings_to_npy(embeddings, npy_path):
    np.save(npy_path, embeddings)
    print(f"[INFO] Embeddings saved to {npy_path}")


def load_embeddings_from_npy(npy_path):
    if not os.path.isfile(npy_path):
        raise FileNotFoundError(f"{npy_path} not found.")
    embeddings = np.load(npy_path)
    print(f"[INFO] Loaded embeddings from {npy_path}, shape: {embeddings.shape}")
    return embeddings


def save_chunks_to_json(chunks, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Chunks saved to {json_path}")


def load_chunks_from_json(json_path):
    if not os.path.isfile(json_path):
        print(f"[WARNING] {json_path} not found. Returning empty list.")
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"[INFO] Loaded {len(chunks)} chunks from {json_path}.")
    return chunks


def search_faiss_index(query, index, chunks, embeddings, top_k=3, model="text-embedding-ada-002"):
    query_resp = client.embeddings.create(input=[query], model=model)
    query_embedding = np.array(query_resp.data[0].embedding, dtype=np.float32).reshape(1, -1)

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        dist = distances[0][i]
        chunk_text = chunks[idx]
        results.append((chunk_text, dist))
    return results