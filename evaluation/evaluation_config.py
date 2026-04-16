from pathlib import Path

from ragas.metrics import Faithfulness, AnswerCorrectness, ContextPrecision, ContextRecall
from ragas.metrics.base import Metric

# --- Evaluation LLM (OpenAI) ---
# Using gpt-4o-mini instead of Groq because RAGAS metric prompts send the full
# retrieved context to the eval LLM (~8-9K tokens/call), which exceeds Groq's
# 6,000 TPM free-tier cap. gpt-4o-mini on OpenAI handles this comfortably and
# keeps evaluation independent of the production Groq quota.
EVALUATION_LLM_MODEL: str = "gpt-4o-mini"

# --- Evaluation Embedding Model (OpenAI) ---
EVALUATION_EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"

# --- Evaluation query-engine top-k ---
# Retrieve 4 chunks per question during evaluation (matches baseline config).
# Keeping this value small reduces RAGAS prompt size and avoids context-window
# overflows in the evaluation LLM.
EVAL_SIMILARITY_TOP_K: int = 4

# --- RAGAS Metrics ---
EVALUATION_METRICS: list[Metric] = [
    Faithfulness(),
    AnswerCorrectness(),
    ContextPrecision(),
    ContextRecall(),
]

# --- Rate-limit sleep config (seconds) ---
# Groq free tier: ~30 req/min. Each RAGAS question spawns several LLM calls.
SLEEP_BETWEEN_QUESTIONS: int = 8    # pause between querying each question
SLEEP_BETWEEN_EVALUATIONS: int = 65  # pause between RAGAS metric evaluations

# --- Paths ---
EVALUATION_ROOT_PATH: Path = Path(__file__).parent
EVALUATION_RESULTS_PATH: Path = EVALUATION_ROOT_PATH / "evaluation_results/"
EVALUATION_EMBEDDING_CACHE_PATH: Path = (
    EVALUATION_ROOT_PATH.parent / "local_storage/embedding_model/"
)
EXPERIMENTAL_VECTOR_STORES_PATH: Path = (
    EVALUATION_ROOT_PATH.parent / "local_storage/experimental_vector_stores/"
)

# --- Stage 2: Chunking Strategy Configs ---
CHUNKING_STRATEGY_CONFIGS: list[dict[str, int]] = [
    {"size": 512,  "overlap": 50},
    {"size": 768,  "overlap": 115},
    {"size": 1024, "overlap": 200},
]

# --- Stage 3: Reranker Configs ---
RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANKER_CONFIGS: list[dict[str, int]] = [
    {"retriever_k": 10, "reranker_n": 2},
    {"retriever_k": 10, "reranker_n": 5},
    {"retriever_k": 20, "reranker_n": 5},
]

# --- Stage 4: Best reranker config found in Stage 3 ---
# Update this after reviewing Stage 3 results.
BEST_RERANKER_STRATEGY: dict[str, int] = {"retriever_k": 10, "reranker_n": 2}
