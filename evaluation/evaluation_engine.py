import pandas as pd
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from ragas import EvaluationDataset
from ragas.llms import LlamaIndexLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper

from evaluation.evaluation_config import (
    BEST_RERANKER_STRATEGY,
    CHUNKING_STRATEGY_CONFIGS,
    EVAL_SIMILARITY_TOP_K,
    RERANKER_CONFIGS,
    RERANKER_MODEL_NAME,
)
from evaluation.evaluation_helper_functions import (
    generate_qa_dataset,
    get_evaluation_data,
    get_or_build_index,
    evaluate_with_rate_limit,
    save_results,
)
from evaluation.evaluation_model_loader import load_ragas_models
from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.model_loader import get_embedding_model, initialise_evaluation_query_llm


# ---------------------------------------------------------------------------
# Stage 1 — Baseline
# ---------------------------------------------------------------------------

def evaluate_baseline() -> None:
    """Evaluates the RAG system using the defaults in src/config.py."""
    print("\n--- Stage 1: Baseline Evaluation ---")

    llm: Groq = initialise_evaluation_query_llm()
    embed_model: HuggingFaceEmbedding = get_embedding_model()
    questions, ground_truths = get_evaluation_data()
    ragas_llm, ragas_embeddings = load_ragas_models()

    index = get_or_build_index(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        embed_model=embed_model,
    )
    query_engine = index.as_query_engine(
        similarity_top_k=EVAL_SIMILARITY_TOP_K,
        llm=llm,
    )

    dataset: EvaluationDataset = generate_qa_dataset(query_engine, questions, ground_truths)
    results_df: pd.DataFrame = evaluate_with_rate_limit(dataset, ragas_llm, ragas_embeddings)

    results_df["chunk_size"] = CHUNK_SIZE
    results_df["chunk_overlap"] = CHUNK_OVERLAP
    save_results(results_df, "baseline_evaluation")
    print("--- Stage 1 complete ---")


# ---------------------------------------------------------------------------
# Stage 2 — Chunking Strategy
# ---------------------------------------------------------------------------

def evaluate_chunking_strategies() -> None:
    """Evaluates each chunking config in CHUNKING_STRATEGY_CONFIGS."""
    print("\n--- Stage 2: Chunking Strategy Evaluation ---")

    llm: Groq = initialise_evaluation_query_llm()
    embed_model: HuggingFaceEmbedding = get_embedding_model()
    questions, ground_truths = get_evaluation_data()
    ragas_llm, ragas_embeddings = load_ragas_models()

    all_results: list[pd.DataFrame] = []

    for config in CHUNKING_STRATEGY_CONFIGS:
        chunk_size = config["size"]
        chunk_overlap = config["overlap"]
        print(f"\n  Config: chunk_size={chunk_size}, overlap={chunk_overlap}")

        index = get_or_build_index(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embed_model=embed_model,
        )
        query_engine = index.as_query_engine(
            similarity_top_k=EVAL_SIMILARITY_TOP_K,
            llm=llm,
        )

        dataset = generate_qa_dataset(query_engine, questions, ground_truths)
        results_df = evaluate_with_rate_limit(dataset, ragas_llm, ragas_embeddings)

        results_df["chunk_size"] = chunk_size
        results_df["chunk_overlap"] = chunk_overlap
        all_results.append(results_df)

    final_df = pd.concat(all_results, ignore_index=True)
    save_results(final_df, "chunking_evaluation")
    print("--- Stage 2 complete ---")


# ---------------------------------------------------------------------------
# Stage 3 — Reranker
# ---------------------------------------------------------------------------

def evaluate_reranker_strategies() -> None:
    """
    Evaluates each reranker config in RERANKER_CONFIGS using the best
    chunk size from Stage 2 (as set in src/config.py).
    """
    print("\n--- Stage 3: Reranker Strategy Evaluation ---")

    llm: Groq = initialise_evaluation_query_llm()
    embed_model: HuggingFaceEmbedding = get_embedding_model()
    questions, ground_truths = get_evaluation_data()
    ragas_llm, ragas_embeddings = load_ragas_models()

    index = get_or_build_index(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        embed_model=embed_model,
    )

    all_results: list[pd.DataFrame] = []

    for config in RERANKER_CONFIGS:
        retriever_k = config["retriever_k"]
        reranker_n = config["reranker_n"]
        print(f"\n  Config: retriever_k={retriever_k}, reranker_n={reranker_n}")

        retriever = index.as_retriever(similarity_top_k=retriever_k)
        reranker = SentenceTransformerRerank(
            top_n=reranker_n,
            model=RERANKER_MODEL_NAME,
        )
        query_engine = RetrieverQueryEngine.from_args(
            retriever=retriever,
            node_postprocessors=[reranker],
            llm=llm,
        )

        dataset = generate_qa_dataset(query_engine, questions, ground_truths)
        results_df = evaluate_with_rate_limit(dataset, ragas_llm, ragas_embeddings)

        results_df["chunk_size"] = CHUNK_SIZE
        results_df["chunk_overlap"] = CHUNK_OVERLAP
        results_df["retriever_k"] = retriever_k
        results_df["reranker_n"] = reranker_n
        all_results.append(results_df)

    final_df = pd.concat(all_results, ignore_index=True)
    save_results(final_df, "reranker_evaluation")
    print("--- Stage 3 complete ---")


# ---------------------------------------------------------------------------
# Stage 4 — HyDE Query Rewriting
# ---------------------------------------------------------------------------

def evaluate_query_rewriting() -> None:
    """
    Compares the best reranker config with and without HyDE query rewriting.
    Uses BEST_RERANKER_STRATEGY from evaluation_config.py.
    """
    print("\n--- Stage 4: Query Rewriting (HyDE) Evaluation ---")

    llm: Groq = initialise_evaluation_query_llm()
    embed_model: HuggingFaceEmbedding = get_embedding_model()
    questions, ground_truths = get_evaluation_data()
    ragas_llm, ragas_embeddings = load_ragas_models()

    best_retriever_k: int = BEST_RERANKER_STRATEGY["retriever_k"]
    best_reranker_n: int = BEST_RERANKER_STRATEGY["reranker_n"]

    index = get_or_build_index(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        embed_model=embed_model,
    )

    all_results: list[pd.DataFrame] = []

    for use_hyde in [False, True]:
        print(f"\n  Config: use_hyde={use_hyde}")

        retriever = index.as_retriever(similarity_top_k=best_retriever_k)
        reranker = SentenceTransformerRerank(
            top_n=best_reranker_n,
            model=RERANKER_MODEL_NAME,
        )
        base_query_engine = RetrieverQueryEngine.from_args(
            retriever=retriever,
            node_postprocessors=[reranker],
            llm=llm,
        )

        if use_hyde:
            hyde_transform = HyDEQueryTransform(
                llm=llm,
                include_original=True,
            )
            query_engine = TransformQueryEngine(
                query_engine=base_query_engine,
                query_transform=hyde_transform,
            )
        else:
            query_engine = base_query_engine

        dataset = generate_qa_dataset(query_engine, questions, ground_truths)
        results_df = evaluate_with_rate_limit(dataset, ragas_llm, ragas_embeddings)

        results_df["chunk_size"] = CHUNK_SIZE
        results_df["chunk_overlap"] = CHUNK_OVERLAP
        results_df["retriever_k"] = best_retriever_k
        results_df["reranker_n"] = best_reranker_n
        results_df["use_hyde"] = use_hyde
        all_results.append(results_df)

    final_df = pd.concat(all_results, ignore_index=True)
    save_results(final_df, "query_rewrite_evaluation")
    print("--- Stage 4 complete ---")
