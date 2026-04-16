import os

from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from ragas.llms import LlamaIndexLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper

from evaluation.evaluation_config import (
    EVALUATION_LLM_MODEL,
    EVALUATION_EMBEDDING_MODEL_NAME,
)

load_dotenv()


def load_ragas_models() -> tuple[LlamaIndexLLMWrapper, LlamaIndexEmbeddingsWrapper]:
    """
    Returns RAGAS-compatible wrappers for the evaluation LLM and embeddings.

    Uses OpenAI (gpt-4o-mini + text-embedding-3-small) instead of Groq because:
    - RAGAS metric prompts send full retrieved contexts to the eval LLM, which can
      be 8,000–9,000 tokens per call — exceeding Groq free tier's 6,000 TPM cap.
    - OpenAI's tier-1 rate limits (200K TPM for gpt-4o-mini) comfortably handle
      the workload without impacting the production Groq quota.
    """
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")

    print(f"  Loading RAGAS evaluation models (LLM={EVALUATION_LLM_MODEL}, "
          f"Embeddings={EVALUATION_EMBEDDING_MODEL_NAME})...")

    ragas_llm = LlamaIndexLLMWrapper(
        llm=OpenAI(model=EVALUATION_LLM_MODEL, api_key=api_key)
    )
    ragas_embeddings = LlamaIndexEmbeddingsWrapper(
        embeddings=OpenAIEmbedding(
            model=EVALUATION_EMBEDDING_MODEL_NAME, api_key=api_key
        )
    )

    return ragas_llm, ragas_embeddings
