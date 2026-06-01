import os
import pickle
import numpy as np
import faiss

from sentence_transformers import (
    SentenceTransformer
)

from utils.prompts import CHAT_PROMPT
from utils.gemini_utils import generate_content


# =========================================
# EMBEDDING MODEL
# =========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================================
# VECTOR STORE PATH
# =========================================

VECTOR_DIR = "data/vector_store"

os.makedirs(
    VECTOR_DIR,
    exist_ok=True
)

INDEX_FILE = os.path.join(
    VECTOR_DIR,
    "faiss_index.bin"
)

CHUNK_FILE = os.path.join(
    VECTOR_DIR,
    "chunks.pkl"
)

# =========================================
# CHUNKING
# =========================================

def chunk_text(
    text,
    chunk_size=500,
    overlap=100
):
    """
    Split transcript into chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = words[start:end]

        chunks.append(
            " ".join(chunk)
        )

        start += (
            chunk_size - overlap
        )

    return chunks


# =========================================
# CREATE EMBEDDINGS
# =========================================

def create_embeddings(
    chunks
):
    """
    Create embeddings.
    """

    embeddings = embedding_model.encode(
        chunks,
        show_progress_bar=True
    )

    return np.array(
        embeddings,
        dtype=np.float32
    )


# =========================================
# BUILD VECTOR STORE
# =========================================

def build_vector_store(
    transcript_text
):
    """
    Create FAISS index.
    """

    chunks = chunk_text(
        transcript_text
    )

    embeddings = create_embeddings(
        chunks
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    faiss.write_index(
        index,
        INDEX_FILE
    )

    with open(
        CHUNK_FILE,
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )

    return len(chunks)


# =========================================
# LOAD VECTOR STORE
# =========================================

def load_vector_store():
    """
    Load saved FAISS index.
    """

    if not os.path.exists(
        INDEX_FILE
    ):
        raise FileNotFoundError(
            "Vector store not found."
        )

    index = faiss.read_index(
        INDEX_FILE
    )

    with open(
        CHUNK_FILE,
        "rb"
    ) as f:

        chunks = pickle.load(f)

    return index, chunks


# =========================================
# SEARCH SIMILAR CHUNKS
# =========================================

def retrieve_context(
    question,
    top_k=4
):
    """
    Retrieve most relevant chunks.
    """

    index, chunks = (
        load_vector_store()
    )

    question_embedding = (
        embedding_model.encode(
            [question]
        )
    )

    question_embedding = np.array(
        question_embedding,
        dtype=np.float32
    )

    distances, indices = (
        index.search(
            question_embedding,
            top_k
        )
    )

    retrieved_chunks = []

    for idx in indices[0]:

        if idx < len(chunks):

            retrieved_chunks.append(
                chunks[idx]
            )

    return "\n\n".join(
        retrieved_chunks
    )


# =========================================
# CHAT WITH VIDEO
# =========================================

def ask_video(
    question
):
    """
    RAG question answering.
    """

    context = retrieve_context(
        question
    )

    prompt = CHAT_PROMPT.format(
        context=context,
        question=question
    )

    answer = generate_content(
        prompt
    )

    return answer


# =========================================
# CHECK IF VECTOR STORE EXISTS
# =========================================

def vector_store_exists():

    return (
        os.path.exists(
            INDEX_FILE
        )
        and
        os.path.exists(
            CHUNK_FILE
        )
    )