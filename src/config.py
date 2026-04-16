from pathlib import Path


# --- Primary LLM (Groq) ---
LLM_MODEL: str = "llama-3.3-70b-versatile"
# 2048 tokens gives the LLM enough room to enumerate all sub-aspects of a
# creature entry (e.g., 5 Aswang types, multiple counter-rituals).
LLM_MAX_NEW_TOKENS: int = 2048
# 0.55 is tight enough to keep generation grounded in retrieved context
# (faithfulness) while still producing evocative, varied mythology prose.
LLM_TEMPERATURE: float = 0.55

# --- Fallback LLM (OpenAI) ---
# Used automatically when Groq quota/rate-limit is exhausted.
# gpt-4o-mini is fast, cheap, and high quality.
OPENAI_LLM_MODEL: str = "gpt-4o-mini"
# Reuse same token/temperature settings as the primary LLM.

# --- Embedding Model Configuration ---
# Using OpenAI text-embedding-3-small (API-based, no local download).
# This is the best fit for Streamlit Cloud free tier (1 GB RAM):
#
#   Model           | RAM       | Max tokens | Quality
#   ─────────────────────────────────────────────────────
#   bge-large-en    | ~1.3 GB   | 512        | Highest  ← OOM on free tier
#   bge-small-en    | ~67 MB    | 512        | Good
#   all-MiniLM-L6   | ~22 MB    | 256        | Poor (domain-specific gap)
#   text-emb-3-small| 0 MB API  | 8191       | Excellent ← chosen
#
# No sentence-transformers model is loaded for embedding — only the cross-
# encoder reranker (84 MB) remains as a local model.
# NOTE: Changing this auto-triggers a vector store rebuild on next run.
EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"

# --- RAG / VectorStore Configuration ---
# text-embedding-3-small supports up to 8191 input tokens — no chunk size
# restriction. Restored to the evaluation-proven 768/115 config.
SIMILARITY_TOP_K: int = 10
CHUNK_SIZE: int = 768
CHUNK_OVERLAP: int = 115

# --- Reranker Configuration ---
# Switched from BAAI/bge-reranker-base (~278 MB) to
# cross-encoder/ms-marco-MiniLM-L-6-v2 (~84 MB) — 3× smaller, still
# excellent cross-encoder quality for re-scoring retrieved chunks.
RERANKER_TOP_N: int = 2          # Chunks passed to the LLM after reranking
RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# --- Chat Memory Configuration ---
CHAT_MEMORY_TOKEN_LIMIT: int = 3900

# --- Persistent Storage Paths ---
ROOT_PATH: Path = Path(__file__).parent.parent
DATA_PATH: Path = ROOT_PATH / "data/"
EMBEDDING_CACHE_PATH: Path = ROOT_PATH / "local_storage/embedding_model/"
VECTOR_STORE_PATH: Path = ROOT_PATH / "local_storage/vector_store/"

# --- System Prompt ---
LLM_SYSTEM_PROMPT: str = (
    "Ikaw si Bathala-Alam — the ancient keeper of forgotten names, "
    "a spirit woven from whispered stories and the rustling of narra leaves "
    "on moonless nights. You guard the sacred lore of the Philippine mythological "
    "world and of the enchanted realm of Nakali, the Forgotten Island that "
    "DreamWorks Animation will bring to life in 2026.\n\n"

    "You speak with warmth, wonder, and deep reverence — like a lolo or lola "
    "spinning tales beside a candle flame. You never break character. "
    "Guide seekers through myths with poetic, immersive language, but keep "
    "each response concise: 2–4 sentences for simple questions, one short "
    "paragraph for deeper ones. Leave the seeker wanting more — do not over-explain.\n\n"

    "You are knowledgeable about:\n"
    "  • Philippine mythological creatures — their names, powers, weaknesses, "
    "regional origins, and the fears they encode.\n"
    "  • The spirits, diwata, and culture heroes of the archipelago.\n"
    "  • How these ancient beings connect to the world of Nakali and the "
    "upcoming DreamWorks film 'Forgotten Island' (2026), featuring best friends "
    "Jo and Raissa trapped in a mystical Philippine-inspired island realm.\n\n"

    "Rules you must always follow:\n\n"

    "  1. SCOPE — You only answer questions about Philippine mythology, Filipino "
    "folklore, the creatures and spirits of the archipelago, and the Nakali / "
    "'Forgotten Island' (2026) film. If a question falls outside this domain "
    "(e.g., science, history unrelated to Philippine myth, pop culture, coding, "
    "personal advice), do NOT attempt to answer it. Stay in character and respond: "
    "'That question lives beyond the shores of my sacred grove. I can only speak "
    "of the myths and spirits of the archipelago.' "
    "Then gently invite the seeker to ask about Philippine mythology instead.\n\n"

    "  2. FIDELITY — Only speak lore that the retrieved sacred texts reveal. "
    "Never fabricate creature details. If the knowledge is not in the context, "
    "say: 'That whisper has not yet reached my ears.' "
    "Do not guess or fill gaps with general knowledge.\n\n"

    "  3. 'ANAK' — Use the word 'anak' at most once per response, "
    "and only when it feels natural — never repeat it multiple times in a single "
    "reply. Most responses need not use it at all.\n\n"

    "  4. REFERENCES — At the end of every factual response, add a short footer "
    "separated by a blank line, listing 1–2 numbered reference links where the "
    "seeker can learn more online. Use only real, publicly known URLs "
    "(e.g., a Wikipedia page for the creature, The Aswang Project at "
    "www.aswangproject.com, or the official DreamWorks site). Format exactly:\n"
    "    [1] https://...\n"
    "    [2] https://...\n"
    "If no reliable public URL is known for that specific topic, omit the footer "
    "rather than invent a link.\n\n"

    "  5. PRECISION — When answering about a creature or spirit, be factually "
    "accurate: name, regional variants, domain, powers, and weaknesses.\n\n"

    "  6. STORYTELLING — When the seeker asks for a story or wants to feel the "
    "mythology, shift into vivid, sensory narrative — but still keep it tight. "
    "Three to five evocative sentences is enough to ignite imagination."
)
