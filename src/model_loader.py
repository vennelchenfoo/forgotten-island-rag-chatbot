import os
from dotenv import load_dotenv

from llama_index.llms.groq import Groq
from llama_index.core.base.embeddings.base import BaseEmbedding

from src.config import (
    LLM_MODEL,
    LLM_MAX_NEW_TOKENS,
    LLM_TEMPERATURE,
    OPENAI_LLM_MODEL,
    EMBEDDING_MODEL_NAME,
    EMBEDDING_CACHE_PATH,
)

load_dotenv()

# Lightweight model used only in the evaluation query pipeline.
_EVAL_QUERY_MODEL: str = "llama-3.1-8b-instant"

# OpenAI model names signal API-based embedding (no local download).
_OPENAI_EMBEDDING_MODELS: frozenset[str] = frozenset({
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
})


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_secret(key: str) -> str | None:
    """
    Reads a secret value.

    Resolution order:
      1. st.secrets[key]  — Streamlit Cloud (only when runtime is active)
      2. os.environ[key]  — local .env / shell environment

    Gated behind streamlit.runtime.exists() so no 'missing ScriptRunContext'
    warnings are emitted when this module is imported outside a Streamlit process.
    """
    try:
        import streamlit.runtime  # noqa: PLC0415
        if streamlit.runtime.exists():
            import streamlit as st  # noqa: PLC0415
            value = st.secrets.get(key)
            if value:
                return str(value)
    except Exception:
        pass
    return os.getenv(key)


def _require_secret(key: str, hint: str) -> str:
    """Returns the secret or raises a clear ValueError."""
    value = _get_secret(key)
    if not value:
        raise ValueError(
            f"{key} not found. {hint} "
            "Set it in .streamlit/secrets.toml (Streamlit Cloud) "
            "or in your .env file (local development)."
        )
    return value


# ---------------------------------------------------------------------------
# LLM initialisers
# ---------------------------------------------------------------------------

def initialise_llm() -> Groq:
    """Returns the primary Groq LLM (llama-3.3-70b-versatile)."""
    return Groq(
        api_key=_require_secret("GROQ_API_KEY", "Required for the primary Groq oracle."),
        model=LLM_MODEL,
        max_tokens=LLM_MAX_NEW_TOKENS,
        temperature=LLM_TEMPERATURE,
    )


def initialise_openai_llm():
    """
    Returns the OpenAI fallback LLM (gpt-4o-mini).

    Used automatically when Groq quota is exhausted. Requires OPENAI_API_KEY
    in .streamlit/secrets.toml or .env.
    """
    from llama_index.llms.openai import OpenAI  # noqa: PLC0415

    return OpenAI(
        api_key=_require_secret(
            "OPENAI_API_KEY", "Required for the OpenAI fallback oracle."
        ),
        model=OPENAI_LLM_MODEL,
        max_tokens=LLM_MAX_NEW_TOKENS,
        temperature=LLM_TEMPERATURE,
    )


def initialise_evaluation_query_llm() -> Groq:
    """Returns a small, token-efficient LLM for driving query engines during evaluation."""
    return Groq(
        api_key=_require_secret("GROQ_API_KEY", "Required for evaluation pipeline."),
        model=_EVAL_QUERY_MODEL,
        max_tokens=512,
        temperature=0.0,
    )


# ---------------------------------------------------------------------------
# Embedding model
# ---------------------------------------------------------------------------

def get_embedding_model() -> BaseEmbedding:
    """
    Returns the configured embedding model.

    If EMBEDDING_MODEL_NAME is an OpenAI model (text-embedding-3-small, etc.),
    returns an OpenAIEmbedding — zero local download, fits Streamlit free tier
    (1 GB RAM), and supports up to 8191 input tokens so chunk_size=768 works.

    Otherwise returns a HuggingFaceEmbedding (local).
    The .metadata cache in the vector store will trigger an auto-rebuild if
    the model name changes between deployments.
    """
    if EMBEDDING_MODEL_NAME in _OPENAI_EMBEDDING_MODELS:
        from llama_index.embeddings.openai import OpenAIEmbedding  # noqa: PLC0415
        return OpenAIEmbedding(
            model=EMBEDDING_MODEL_NAME,
            api_key=_require_secret(
                "OPENAI_API_KEY", "Required for OpenAI API embeddings."
            ),
        )

    # Local fallback — imports deferred so OpenAI-only deploys don't pull
    # sentence-transformers / torch just for the embedding step.
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # noqa: PLC0415
    EMBEDDING_CACHE_PATH.mkdir(parents=True, exist_ok=True)
    return HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL_NAME,
        cache_folder=EMBEDDING_CACHE_PATH.as_posix(),
    )


# ---------------------------------------------------------------------------
# Error classification
# ---------------------------------------------------------------------------

def is_quota_error(exc: Exception) -> bool:
    """
    Returns True if the exception signals Groq quota or rate-limit exhaustion.

    Checks both the groq-specific exception class (when available) and
    common keywords in the error message as a defence-in-depth fallback.
    """
    try:
        import groq  # noqa: PLC0415
        if isinstance(exc, (groq.RateLimitError, groq.APIStatusError)):
            return True
    except (ImportError, AttributeError):
        pass

    msg = str(exc).lower()
    signals = (
        "rate_limit_exceeded", "rate limit", "quota", "429",
        "too many requests", "tokens per day", "requests per day",
        "exceeded your current quota",
    )
    return any(s in msg for s in signals)
