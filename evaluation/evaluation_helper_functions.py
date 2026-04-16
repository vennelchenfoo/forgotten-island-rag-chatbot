import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.llms import LlamaIndexLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper

from evaluation.evaluation_config import (
    EVALUATION_METRICS,
    EVALUATION_RESULTS_PATH,
    EXPERIMENTAL_VECTOR_STORES_PATH,
    SLEEP_BETWEEN_EVALUATIONS,
    SLEEP_BETWEEN_QUESTIONS,
)
from evaluation.evaluation_questions import EVALUATION_DATA
from src.config import DATA_PATH


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def get_evaluation_data() -> tuple[list[str], list[str]]:
    """Unpacks EVALUATION_DATA into parallel lists of questions and ground truths."""
    questions = [item["question"] for item in EVALUATION_DATA]
    ground_truths = [item["ground_truth"] for item in EVALUATION_DATA]
    return questions, ground_truths


# ---------------------------------------------------------------------------
# Index management
# ---------------------------------------------------------------------------

def get_or_build_index(
    chunk_size: int,
    chunk_overlap: int,
    embed_model: HuggingFaceEmbedding,
) -> VectorStoreIndex:
    """
    Returns a VectorStoreIndex for the given chunk config.
    Loads from disk if a cached version exists; otherwise builds and saves one.
    Each config gets its own subdirectory under experimental_vector_stores/.
    """
    store_id = f"vs_chunk{chunk_size}_overlap{chunk_overlap}"
    store_path: Path = EXPERIMENTAL_VECTOR_STORES_PATH / store_id
    store_path.mkdir(parents=True, exist_ok=True)

    if any(store_path.iterdir()):
        print(f"  Loading cached index: {store_id}")
        storage_context = StorageContext.from_defaults(persist_dir=store_path.as_posix())
        return load_index_from_storage(storage_context, embed_model=embed_model)

    print(f"  Building new index: {store_id} (chunk={chunk_size}, overlap={chunk_overlap})")
    documents = SimpleDirectoryReader(input_dir=DATA_PATH.as_posix()).load_data()
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[splitter],
        embed_model=embed_model,
        show_progress=True,
    )
    index.storage_context.persist(persist_dir=store_path.as_posix())
    return index


# ---------------------------------------------------------------------------
# Dataset generation
# ---------------------------------------------------------------------------

def generate_qa_dataset(
    query_engine: BaseQueryEngine,
    questions: list[str],
    ground_truths: list[str],
) -> EvaluationDataset:
    """
    Runs each question through the query engine to collect answers and
    source contexts, then returns a RAGAS EvaluationDataset.
    """
    samples: list[SingleTurnSample] = []
    n = len(questions)

    for i, (question, ground_truth) in enumerate(zip(questions, ground_truths)):
        print(f"  [{i + 1}/{n}] Querying: '{question[:60]}...'")
        response = query_engine.query(question)

        answer: str = str(response)
        contexts: list[str] = [
            node.node.get_content() for node in response.source_nodes
        ]

        samples.append(
            SingleTurnSample(
                user_input=question,
                response=answer,
                retrieved_contexts=contexts,
                reference=ground_truth,
            )
        )

        if i < n - 1:
            time.sleep(SLEEP_BETWEEN_QUESTIONS)

    return EvaluationDataset(samples=samples)


# ---------------------------------------------------------------------------
# Evaluation runners
# ---------------------------------------------------------------------------

def evaluate_with_rate_limit(
    dataset: EvaluationDataset,
    ragas_llm: LlamaIndexLLMWrapper,
    ragas_embeddings: LlamaIndexEmbeddingsWrapper,
) -> pd.DataFrame:
    """
    Evaluates the dataset one sample at a time to stay within Groq's free-tier
    rate limits. Sleeps between each sample evaluation.
    """
    print(f"  Running RAGAS evaluation ({len(dataset.samples)} samples, rate-limited)...")
    partial_results: list[pd.DataFrame] = []

    for i, sample in enumerate(dataset.samples):
        print(f"  Evaluating sample {i + 1}/{len(dataset.samples)}...")
        single_dataset = EvaluationDataset(samples=[sample])

        result = evaluate(
            dataset=single_dataset,
            metrics=EVALUATION_METRICS,
            llm=ragas_llm,
            embeddings=ragas_embeddings,
            show_progress=False,
            raise_exceptions=False,
        )
        partial_results.append(result.to_pandas())

        if i < len(dataset.samples) - 1:
            print(f"  Sleeping {SLEEP_BETWEEN_EVALUATIONS}s (rate limit)...")
            time.sleep(SLEEP_BETWEEN_EVALUATIONS)

    return pd.concat(partial_results, ignore_index=True)


def evaluate_without_rate_limit(
    dataset: EvaluationDataset,
    ragas_llm: LlamaIndexLLMWrapper,
    ragas_embeddings: LlamaIndexEmbeddingsWrapper,
) -> pd.DataFrame:
    """
    Evaluates the full dataset in one batch. Use only when your API plan
    has no strict rate limits (e.g., local models or paid tiers).
    """
    print("  Running RAGAS evaluation (batch mode)...")
    result = evaluate(
        dataset=dataset,
        metrics=EVALUATION_METRICS,
        llm=ragas_llm,
        embeddings=ragas_embeddings,
        show_progress=True,
        raise_exceptions=False,
    )
    return result.to_pandas()


# ---------------------------------------------------------------------------
# Results persistence
# ---------------------------------------------------------------------------

def save_results(results_df: pd.DataFrame, filename_prefix: str) -> None:
    """
    Saves a detailed CSV (one row per question) and a summary CSV
    (averages per config group) into evaluation_results/.
    """
    EVALUATION_RESULTS_PATH.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    metric_cols = ["faithfulness", "answer_correctness", "context_precision", "context_recall"]
    available_metrics = [c for c in metric_cols if c in results_df.columns]

    # Detailed: every question row
    detailed_path = EVALUATION_RESULTS_PATH / f"{filename_prefix}_detailed_{timestamp}.csv"
    results_df.to_csv(detailed_path, index=False)
    print(f"  Saved detailed results → {detailed_path.name}")

    # Summary: group by scalar (hashable) non-metric columns, average the metrics
    def _is_scalar_col(col: str) -> bool:
        return results_df[col].map(lambda v: not isinstance(v, (list, dict))).all()

    group_cols = [
        c for c in results_df.columns
        if c not in available_metrics and _is_scalar_col(c)
    ]
    if group_cols:
        summary_df = results_df.groupby(group_cols)[available_metrics].mean().reset_index()
    else:
        summary_df = results_df[available_metrics].mean().to_frame().T

    summary_path = EVALUATION_RESULTS_PATH / f"{filename_prefix}_summary_{timestamp}.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"  Saved summary results  → {summary_path.name}")
    print(summary_df.to_string(index=False, float_format="{:.4f}".format))
