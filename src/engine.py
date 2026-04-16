from pathlib import Path

from llama_index.core import (
    StorageContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.memory import ChatSummaryMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.retrievers import TransformRetriever
from llama_index.core.schema import Document
from llama_index.llms.groq import Groq

from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CHAT_MEMORY_TOKEN_LIMIT,
    DATA_PATH,
    EMBEDDING_MODEL_NAME,
    LLM_SYSTEM_PROMPT,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_N,
    SIMILARITY_TOP_K,
    VECTOR_STORE_PATH,
)
from src.model_loader import get_embedding_model, initialise_llm


# --- Vector Store Metadata ---
# We store the embedding model name alongside the vector store so that if
# EMBEDDING_MODEL_NAME is changed in config, we automatically detect the
# mismatch and rebuild rather than silently serving incorrect results.
_METADATA_FILE: Path = VECTOR_STORE_PATH / ".metadata"


def _read_cached_embedding_model() -> str | None:
    """Returns the embedding model name from the last vector store build, or None."""
    if _METADATA_FILE.exists():
        return _METADATA_FILE.read_text(encoding="utf-8").strip()
    return None


def _write_vector_store_metadata() -> None:
    """Persists the current embedding model name to the metadata file."""
    _METADATA_FILE.write_text(EMBEDDING_MODEL_NAME, encoding="utf-8")


def _is_vector_store_stale() -> bool:
    """Returns True if the cached vector store was built with a different embedding model."""
    return _read_cached_embedding_model() != EMBEDDING_MODEL_NAME


# --- Vector Store Management ---

def _create_new_vector_store(embed_model: BaseEmbedding) -> VectorStoreIndex:
    """Builds a vector store from documents in data/, persists it to disk, and returns it."""
    print("  Building vector store from the sacred texts in data/...")

    documents: list[Document] = SimpleDirectoryReader(
        input_dir=DATA_PATH.as_posix()
    ).load_data()

    if not documents:
        raise ValueError(
            f"No documents found in {DATA_PATH}. "
            "Add your Philippine mythology markdown files and try again."
        )

    text_splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[text_splitter],
        embed_model=embed_model,
        show_progress=True,
    )

    index.storage_context.persist(persist_dir=VECTOR_STORE_PATH.as_posix())
    _write_vector_store_metadata()
    print("  Vector store built and saved.")
    return index


def get_vector_store(embed_model: BaseEmbedding) -> VectorStoreIndex:
    """
    Returns a VectorStoreIndex, loading from disk when possible.

    Automatically rebuilds if:
    - No vector store exists yet, or
    - The cached store was built with a different embedding model.
    """
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)

    store_has_content = any(
        p for p in VECTOR_STORE_PATH.iterdir() if p.name != ".metadata"
    )

    if store_has_content and not _is_vector_store_stale():
        print("  Loading existing vector store from disk...")
        storage_context = StorageContext.from_defaults(
            persist_dir=VECTOR_STORE_PATH.as_posix()
        )
        return load_index_from_storage(storage_context, embed_model=embed_model)

    if store_has_content:
        print(
            f"  Embedding model changed to '{EMBEDDING_MODEL_NAME}'. "
            "Rebuilding vector store..."
        )

    return _create_new_vector_store(embed_model)


# --- Chat Engine ---

def get_chat_engine(
    llm: Groq,
    embed_model: BaseEmbedding,
) -> CondensePlusContextChatEngine:
    """
    Builds and returns the full advanced RAG chat engine.

    Pipeline stages (applied in order per query):
      1. HyDE  — generates a hypothetical answer to enrich the query
                 embedding, bridging vocabulary gaps between casual
                 questions and formal mythology text.
      2. Retriever — broad vector-similarity search (top SIMILARITY_TOP_K).
      3. Reranker  — cross-encoder re-scores candidates; only RERANKER_TOP_N
                     highest-quality chunks reach the LLM.
      4. CondensePlusContextChatEngine — condenses conversation history into
                 a standalone question before each retrieval step, so
                 multi-turn context is handled correctly throughout.
      5. ChatSummaryMemoryBuffer — summarises older turns to stay within
                 the token budget while preserving meaningful context.
    """
    vector_index: VectorStoreIndex = get_vector_store(embed_model)

    # Stage 1: HyDE — enrich query with hypothetical answer embedding
    base_retriever: BaseRetriever = vector_index.as_retriever(
        similarity_top_k=SIMILARITY_TOP_K
    )
    hyde = HyDEQueryTransform(
        llm=llm,
        include_original=True,  # searches with BOTH hypothetical answer AND real question
    )
    hyde_retriever = TransformRetriever(
        retriever=base_retriever,
        query_transform=hyde,
    )

    # Stage 2: Cross-encoder reranker — keeps only the RERANKER_TOP_N best chunks
    reranker = SentenceTransformerRerank(
        top_n=RERANKER_TOP_N,
        model=RERANKER_MODEL_NAME,
    )

    # Stage 3: Memory — summarises older turns to stay within token budget
    memory = ChatSummaryMemoryBuffer.from_defaults(
        token_limit=CHAT_MEMORY_TOKEN_LIMIT,
        llm=llm,
    )

    # Stage 4: Assemble — condenses history into a standalone question before retrieval
    chat_engine = CondensePlusContextChatEngine(
        retriever=hyde_retriever,
        llm=llm,
        memory=memory,
        system_prompt=LLM_SYSTEM_PROMPT,
        node_postprocessors=[reranker],
    )

    return chat_engine


# --- Main Chat Loop ---

def main_chat_loop() -> None:
    """Initialises all components and runs the Philippine Mythology RAG chatbot."""
    print("\n--- Awakening the spirits... ---")
    llm: Groq = initialise_llm()
    embed_model: BaseEmbedding = get_embedding_model()

    chat_engine: CondensePlusContextChatEngine = get_chat_engine(
        llm=llm,
        embed_model=embed_model,
    )

    print("\n" + "=" * 60)
    print("  BATHALA-ALAM — Guardian of Philippine Mythological Lore")
    print("=" * 60)
    print(
        "\nMagandang araw, anak. I am Bathala-Alam, keeper of ancient whispers.\n"
        "Ask me of the creatures that stalk the night, the spirits of forest\n"
        "and sea, the heroes and gods of the blessed archipelago —\n"
        "or how these legends live again in the world of Nakali.\n"
    )
    print("  Type 'exit' or 'quit' to leave.\n")
    print("-" * 60)

    while True:
        try:
            user_input: str = input("\nSeeker: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nBathala-Alam: The wind carries you away, anak. Paalam.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print(
                "\nBathala-Alam: May the old stories walk beside you on your path. Paalam."
            )
            break

        try:
            response = chat_engine.chat(user_input)
            print(f"\nBathala-Alam: {response}")
        except Exception as e:
            print(f"\n[Error] The spirits are unsettled: {e}")
            print("Please try rephrasing your question.")
