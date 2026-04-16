"""
Forgotten Island — Bathala-Alam
A Streamlit oracle for Philippine Mythology and the mystical world of Nakali.

Deployment: Streamlit Community Cloud (GitHub-based, free tier — 1 GB RAM)
Engine: LlamaIndex RAG · Groq (llama-3.3-70b-versatile, fallback: OpenAI gpt-4o-mini)
Embedding: OpenAI text-embedding-3-small (API-based, 0 MB local model)
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2 (84 MB local)

Memory budget:
  Python + Streamlit + LlamaIndex  ~250 MB
  PyTorch (CPU, reranker only)      ~200 MB
  ms-marco reranker weights          ~84 MB
  Vector index (in RAM)              ~10 MB
  ─────────────────────────────────────────
  Total                             ~544 MB  ← well within 1 GB free tier
"""
from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Forgotten Island — Bathala-Alam",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**Forgotten Island — Bathala-Alam**\n\n"
            "An AI oracle steeped in Philippine mythology, keeper of the sacred "
            "lore of Nakali.\n\n"
            "Powered by LlamaIndex · Groq · Streamlit"
        )
    },
)

# ---------------------------------------------------------------------------
# CSS — Dark Mystic Philippine Theme
# ---------------------------------------------------------------------------
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Raleway:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* === Design tokens === */
:root {
  --bg:          #070710;
  --bg2:         #0c0c1a;
  --bg3:         #101025;
  --gold:        #c9a227;
  --gold-dim:    #7a601a;
  --gold-faint:  rgba(201,162,39,0.12);
  --jade:        #2d6a4f;
  --jade-light:  #40916c;
  --jade-faint:  rgba(45,106,79,0.12);
  --parchment:   #e8d5b7;
  --muted:       #9a8060;
  --glow-gold:   0 0 18px rgba(201,162,39,0.35);
  --glow-jade:   0 0 14px rgba(64,145,108,0.4);
  --border-gold: 1px solid rgba(201,162,39,0.22);
  --border-jade: 1px solid rgba(64,145,108,0.25);
}

/* === Global reset === */
html, body {
  background: var(--bg) !important;
  color: var(--parchment) !important;
}

[data-testid="stAppViewContainer"] {
  background: radial-gradient(
    ellipse at 30% 0%,
    rgba(12,10,35,0.95) 0%,
    var(--bg) 55%
  ) !important;
  min-height: 100vh;
}

[data-testid="stMain"] {
  background: transparent !important;
}

[data-testid="stMainBlockContainer"] {
  padding-top: 0 !important;
}

/* === Typography === */
*, p, li, span, label, div {
  font-family: 'Raleway', sans-serif;
  color: var(--parchment);
}

h1, h2, h3, h4 {
  font-family: 'Cinzel', serif !important;
  color: var(--gold) !important;
  text-shadow: var(--glow-gold) !important;
  letter-spacing: 0.06em !important;
}

a { color: var(--jade-light) !important; }
a:hover { color: var(--gold) !important; text-decoration: none !important; }

/* === Sidebar === */
[data-testid="stSidebar"] {
  background: linear-gradient(
    180deg,
    #050510 0%,
    #080f0c 45%,
    #050510 100%
  ) !important;
  border-right: var(--border-gold) !important;
}

[data-testid="stSidebarContent"] {
  padding: 0 !important;
}

/* === Chat messages === */
[data-testid="stChatMessage"] {
  background: var(--bg2) !important;
  border: var(--border-gold) !important;
  border-radius: 10px !important;
  margin-bottom: 14px !important;
  padding: 14px 18px !important;
  box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}

/* User message — jade tint */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
  border-color: rgba(64,145,108,0.28) !important;
  background: linear-gradient(135deg, #0a0f0c, var(--bg2)) !important;
}

/* === Chat input === */
[data-testid="stChatInput"] {
  background: var(--bg2) !important;
  border-top: var(--border-gold) !important;
  padding: 12px !important;
}

[data-testid="stChatInput"] textarea {
  background: var(--bg3) !important;
  border: var(--border-gold) !important;
  color: var(--parchment) !important;
  font-family: 'Raleway', sans-serif !important;
  border-radius: 8px !important;
  padding: 10px 14px !important;
}

[data-testid="stChatInput"] textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: var(--glow-gold) !important;
  outline: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
  color: var(--muted) !important;
  font-style: italic !important;
}

/* === Buttons === */
.stButton > button {
  background: transparent !important;
  border: var(--border-gold) !important;
  color: var(--gold) !important;
  font-family: 'Raleway', sans-serif !important;
  font-size: 0.72rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.04em !important;
  padding: 4px 12px !important;
  border-radius: 4px !important;
  transition: all 0.2s ease !important;
  width: 100% !important;
  margin-top: 4px !important;
}

.stButton > button:hover {
  background: var(--gold-faint) !important;
  box-shadow: var(--glow-gold) !important;
  border-color: var(--gold) !important;
  color: var(--gold) !important;
}

.stButton > button:active {
  transform: scale(0.98) !important;
}

/* === Expanders === */
[data-testid="stExpander"] {
  border: var(--border-jade) !important;
  background: rgba(8, 12, 10, 0.8) !important;
  border-radius: 6px !important;
  margin-bottom: 6px !important;
}

[data-testid="stExpander"] > details > summary {
  color: var(--jade-light) !important;
  font-family: 'Cinzel', serif !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.08em !important;
  padding: 8px 12px !important;
}

[data-testid="stExpander"] > details > summary:hover {
  color: var(--gold) !important;
}

[data-testid="stExpander"] > details > summary::marker,
[data-testid="stExpander"] > details > summary::-webkit-details-marker {
  color: var(--jade-light) !important;
}

[data-testid="stExpander"] > details[open] > summary {
  color: var(--gold) !important;
  border-bottom: var(--border-gold) !important;
}

/* === Dividers / HR === */
hr {
  border: none !important;
  border-top: var(--border-gold) !important;
  margin: 12px 0 !important;
  opacity: 0.6 !important;
}

/* === Spinner === */
.stSpinner > div {
  border-top-color: var(--gold) !important;
}

/* === Alert / Error boxes === */
[data-testid="stAlert"] {
  background: rgba(122, 26, 26, 0.2) !important;
  border: 1px solid rgba(122, 26, 26, 0.5) !important;
  border-radius: 8px !important;
}

/* === Scrollbar === */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* === Hide default Streamlit chrome === */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Creature registry — curated for the sidebar
# ---------------------------------------------------------------------------
_CREATURES: dict[str, list[dict]] = {
    "🩸 Shape-Shifters & Night Predators": [
        {
            "name": "Aswang",
            "desc": "Umbrella term for malevolent shape-shifters — vampire, viscera-sucker, weredog, witch, and ghoul — most feared across Visayas.",
            "link": "https://en.wikipedia.org/wiki/Aswang",
        },
        {
            "name": "Manananggal",
            "desc": "Severs its upper torso at night to fly and prey on sleeping victims with an impossibly long, hollow tongue.",
            "link": "https://en.wikipedia.org/wiki/Manananggal",
        },
        {
            "name": "Sigbin",
            "desc": "A silent night-stalker said to walk backward and drain life through its victim's very shadow.",
            "link": "https://en.wikipedia.org/wiki/Sigbin",
        },
        {
            "name": "Tiktik",
            "desc": "An aswang whose namesake 'tik-tik' call grows louder when the creature is farther away — a cruel and deadly deception.",
            "link": "https://en.wikipedia.org/wiki/Tiktik_(folklore)",
        },
        {
            "name": "Bal-bal",
            "desc": "A ghoulish scavenger that steals freshly buried corpses from graves, replacing them with banana trunks.",
            "link": "https://en.wikipedia.org/wiki/Bal-bal",
        },
    ],
    "🌿 Forest & Mountain Spirits": [
        {
            "name": "Kapre",
            "desc": "A tobacco-smoking giant who dwells in ancient balete and acacia trees. Terrifying — yet sometimes a loyal companion.",
            "link": "https://en.wikipedia.org/wiki/Kapre",
        },
        {
            "name": "Tikbalang",
            "desc": "A horse-headed trickster that leads travelers astray at crossroads. Taming it requires stealing three golden mane hairs.",
            "link": "https://en.wikipedia.org/wiki/Tikbalang",
        },
        {
            "name": "Nuno sa Punso",
            "desc": "An elder spirit inhabiting anthills. Disturbing its mound without asking permission invites illness and misfortune.",
            "link": "https://en.wikipedia.org/wiki/Nuno_sa_punso",
        },
        {
            "name": "Duwende",
            "desc": "Small goblin-like spirits — white ones grant luck, black ones sow chaos. Regular offerings keep the peace.",
            "link": "https://en.wikipedia.org/wiki/Duwende",
        },
        {
            "name": "Maria Makiling",
            "desc": "The enchanted diwata of Mount Makiling. She appears as a breathtaking woman with wild flowers in her hair, guardian of her sacred mountain.",
            "link": "https://en.wikipedia.org/wiki/Maria_Makiling",
        },
        {
            "name": "Alan",
            "desc": "Winged forest spirits with backward-pointing fingers. They hang from branches and raise children from discarded placentas.",
            "link": "https://en.wikipedia.org/wiki/Alan_(Philippine_mythology)",
        },
        {
            "name": "Anggitay",
            "desc": "A horse-bodied woman with a unicorn horn, seen perched on branches during sunshowers — the Philippine counterpart of the centaur.",
            "link": "https://en.wikipedia.org/wiki/Anggitay",
        },
    ],
    "🌊 Water & Sea Beings": [
        {
            "name": "Bakunawa",
            "desc": "A colossal sea serpent that swallows the moon. Ancient Filipinos banged pots and drums to make it spit the moon back out.",
            "link": "https://en.wikipedia.org/wiki/Bakunawa",
        },
        {
            "name": "Sirena",
            "desc": "Philippine mermaids dwelling in rivers and seas, luring sailors and fishermen with songs of impossible beauty.",
            "link": "https://en.wikipedia.org/wiki/Sirena_(Philippines)",
        },
        {
            "name": "Siyokoy",
            "desc": "Scaled mermen draped in green tendrils who drag victims to a watery grave — the feared dark twin of the sirena.",
            "link": "https://en.wikipedia.org/wiki/Siyokoy",
        },
        {
            "name": "Berberoka",
            "desc": "A water monster that drains ponds dry to expose fish, then surges back to drown the fishermen who rush in.",
            "link": "https://en.wikipedia.org/wiki/Berberoka",
        },
        {
            "name": "Magindara",
            "desc": "A fierce Bicolano mermaid spirit — both protectress of the seas and deadly to those who fish without reverence.",
            "link": "https://en.wikipedia.org/wiki/Magindara",
        },
    ],
    "⭐ Sky & Celestial Beings": [
        {
            "name": "Minokawa",
            "desc": "A sun-obscuring sky dragon with mirror-bright feathers, eyes like steel shields, and a beak that can swallow the sun whole.",
            "link": "https://en.wikipedia.org/wiki/Minokawa",
        },
        {
            "name": "Galura",
            "desc": "The Philippine thunderbird — a storm eagle of immense power who commands wind and lightning across the sky.",
            "link": "https://en.wikipedia.org/wiki/Galura",
        },
        {
            "name": "Santelmo",
            "desc": "Wandering orbs of ghostly fire seen over marshes and at sea — the trapped souls of the unburied dead.",
            "link": "https://en.wikipedia.org/wiki/St._Elmo%27s_fire",
        },
    ],
    "👻 Ghosts & Ancestor Spirits": [
        {
            "name": "Tiyanak",
            "desc": "A demon wearing the face of an infant. It cries in the dark forest to lure travelers before revealing its true, hideous form.",
            "link": "https://en.wikipedia.org/wiki/Tiyanak",
        },
        {
            "name": "Bangungot",
            "desc": "The nightmare demon — it sits on a sleeper's chest, crushing the breath from them until they die in the night.",
            "link": "https://en.wikipedia.org/wiki/Bangungot",
        },
        {
            "name": "Multo",
            "desc": "The Filipino ghost — a restless spirit clinging to the world of the living due to unfinished grief, vengeance, or violent death.",
            "link": "https://en.wikipedia.org/wiki/Multo",
        },
    ],
    "✨ Divine Beings & Diwata": [
        {
            "name": "Bathala",
            "desc": "The supreme deity of the Tagalog people — creator of earth, sky, and all of humanity, enthroned in the highest heavens.",
            "link": "https://en.wikipedia.org/wiki/Bathala",
        },
        {
            "name": "Diwata",
            "desc": "Benevolent nature spirits and semi-divine beings who inhabit and protect mountains, rivers, forests, and the sea.",
            "link": "https://en.wikipedia.org/wiki/Diwata",
        },
        {
            "name": "Anito",
            "desc": "Ancestral spirits and nature deities venerated in pre-colonial Philippines through ritual offerings and sacred invocation.",
            "link": "https://en.wikipedia.org/wiki/Anito",
        },
    ],
}

# ---------------------------------------------------------------------------
# Opening message from Bathala-Alam
# ---------------------------------------------------------------------------
_GREETING = (
    "Magandang araw, seeker. I am **Bathala-Alam** — keeper of forgotten names, "
    "a spirit woven from whispered stories and the rustling of narra leaves "
    "on moonless nights.\n\n"
    "Ask me of the creatures that stalk the night, the spirits of forest and sea, "
    "the heroes and gods of the blessed archipelago — or perhaps the mystical "
    "world of **Nakali**, the Forgotten Island that *DreamWorks Animation* will "
    "bring to life in 2026.\n\n"
    "*Browse the creatures in the side panel, or simply ask. The ancient grove awaits...*"
)

# ---------------------------------------------------------------------------
# Session state bootstrap
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = [
        {"role": "assistant", "content": _GREETING}
    ]

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = None

if "engine_error" not in st.session_state:
    st.session_state.engine_error: str | None = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question: str | None = None

if "use_openai" not in st.session_state:
    # Flips to True automatically when Groq quota is exhausted
    st.session_state.use_openai: bool = False


# ---------------------------------------------------------------------------
# Chat engine — heavy resources cached, stateful engine per session
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _load_shared_resources():
    """
    Loads and caches across all sessions:
      • Groq LLM client (API-based, no local model)
      • OpenAI embedding model (API-based, no local model)
      • Vector index (pre-built, loaded from local_storage/vector_store/)

    Runs only once per Streamlit server process.
    """
    from src.model_loader import get_embedding_model, initialise_llm
    from src.engine import get_vector_store

    llm = initialise_llm()
    embed_model = get_embedding_model()
    vector_index = get_vector_store(embed_model)
    return llm, embed_model, vector_index


def _build_session_engine(use_openai: bool = False):
    """
    Builds a fresh CondensePlusContextChatEngine for this user session.

    Parameters
    ----------
    use_openai : bool
        False (default) — use Groq as the primary LLM.
        True            — use OpenAI gpt-4o-mini as the fallback LLM.
                          Triggered automatically on Groq quota exhaustion.

    Heavy, stateless resources (embedding model, vector index) are always
    reused from the @st.cache_resource pool.  Stateful components (memory
    buffer, reranker instance) are always fresh per session.
    """
    from llama_index.core.chat_engine import CondensePlusContextChatEngine
    from llama_index.core.indices.query.query_transform import HyDEQueryTransform
    from llama_index.core.memory import ChatSummaryMemoryBuffer
    from llama_index.core.postprocessor import SentenceTransformerRerank
    from llama_index.core.retrievers import TransformRetriever
    from src.config import (
        SIMILARITY_TOP_K,
        RERANKER_TOP_N,
        RERANKER_MODEL_NAME,
        CHAT_MEMORY_TOKEN_LIMIT,
        LLM_SYSTEM_PROMPT,
    )
    from src.model_loader import initialise_openai_llm

    # Vector index is always shared; LLM is provider-dependent
    _, _, vector_index = _load_shared_resources()
    llm = initialise_openai_llm() if use_openai else _load_shared_resources()[0]

    base_retriever = vector_index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)
    hyde = HyDEQueryTransform(llm=llm, include_original=True)
    hyde_retriever = TransformRetriever(retriever=base_retriever, query_transform=hyde)
    reranker = SentenceTransformerRerank(top_n=RERANKER_TOP_N, model=RERANKER_MODEL_NAME)
    memory = ChatSummaryMemoryBuffer.from_defaults(
        token_limit=CHAT_MEMORY_TOKEN_LIMIT, llm=llm
    )
    return CondensePlusContextChatEngine(
        retriever=hyde_retriever,
        llm=llm,
        memory=memory,
        system_prompt=LLM_SYSTEM_PROMPT,
        node_postprocessors=[reranker],
    )


def _ensure_engine() -> bool:
    """Initialises the chat engine on first call. Returns True if ready."""
    if st.session_state.chat_engine is not None:
        return True
    if st.session_state.engine_error is not None:
        return False

    with st.spinner("☽  Awakening the ancient spirits of Nakali..."):
        try:
            st.session_state.chat_engine = _build_session_engine(
                use_openai=st.session_state.use_openai
            )
        except Exception as exc:
            st.session_state.engine_error = str(exc)
            return False
    return True


# ---------------------------------------------------------------------------
# Engine warm-up — runs once per session, before any UI renders
# This ensures the chat input is active immediately on page load.
# ---------------------------------------------------------------------------
_ensure_engine()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:

    # — App header —
    st.markdown(
        """
        <div style="text-align:center; padding:24px 12px 10px;">
            <div style="font-family:'Cinzel',serif; font-size:1.45rem; color:#c9a227;
                        text-shadow:0 0 24px rgba(201,162,39,0.5); line-height:1.25;
                        letter-spacing:0.06em;">
                Forgotten Island
            </div>
            <div style="font-family:'Cinzel',serif; font-size:0.85rem; color:#40916c;
                        letter-spacing:0.2em; margin-top:5px;
                        text-shadow:0 0 12px rgba(64,145,108,0.5);">
                ⊶ BATHALA-ALAM ⊷
            </div>
            <div style="font-family:'Raleway',sans-serif; font-size:0.68rem; color:#9a8060;
                        margin-top:6px; font-style:italic; letter-spacing:0.03em;">
                Oracle of Philippine Mythology
            </div>
        </div>
        <div style="border-bottom:1px solid rgba(201,162,39,0.22);
                    margin:0 20px 18px;"></div>
        """,
        unsafe_allow_html=True,
    )

    # — Official trailer —
    st.markdown(
        """
        <div style="font-family:'Cinzel',serif; font-size:0.7rem; color:#c9a227;
                    letter-spacing:0.12em; text-align:center; margin-bottom:8px;">
            ▶&nbsp; OFFICIAL TRAILER
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden;
                    border-radius:7px; border:1px solid rgba(201,162,39,0.28);
                    margin-bottom:18px; box-shadow:0 0 20px rgba(0,0,0,0.6);">
            <iframe
                src="https://www.youtube.com/embed/a8RHqN93qfo?rel=0&modestbranding=1&color=white"
                style="position:absolute; top:0; left:0; width:100%; height:100%;"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media;
                       gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # — Creatures section header —
    st.markdown(
        """
        <div style="border-top:1px solid rgba(45,106,79,0.3); padding-top:14px;
                    margin-bottom:10px;">
            <div style="font-family:'Cinzel',serif; font-size:0.72rem; color:#40916c;
                        letter-spacing:0.14em; text-align:center;">
                ☽ &nbsp;CREATURES OF NAKALI&nbsp; ☾
            </div>
            <div style="font-family:'Raleway',sans-serif; font-size:0.63rem; color:#6a5040;
                        text-align:center; margin-top:4px; font-style:italic;">
                Click a creature to ask Bathala-Alam
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # — Creature categories —
    for category, creatures in _CREATURES.items():
        with st.expander(category, expanded=False):
            for creature in creatures:
                # Name + description card
                st.markdown(
                    f"""
                    <div style="background:rgba(7,7,16,0.85);
                                border:1px solid rgba(201,162,39,0.14);
                                border-radius:7px 7px 0 0;
                                padding:10px 12px 8px; margin-bottom:0;">
                        <div style="font-family:'Cinzel',serif; font-size:1.0rem;
                                    color:#c9a227; margin-bottom:5px;
                                    text-shadow:0 0 10px rgba(201,162,39,0.25);">
                            {creature['name']}
                        </div>
                        <div style="font-family:'Raleway',sans-serif; font-size:0.7rem;
                                    color:#9a8060; line-height:1.45;">
                            {creature['desc']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Ask button — first
                if st.button(
                    f"✦ Ask Bathala-Alam about {creature['name']}",
                    key=f"ask__{creature['name']}",
                ):
                    st.session_state.pending_question = (
                        f"Tell me about the {creature['name']}."
                    )
                    st.rerun()
                # Learn more link — below button
                st.markdown(
                    f"""
                    <div style="background:rgba(7,7,16,0.85);
                                border:1px solid rgba(201,162,39,0.14);
                                border-top:none; border-radius:0 0 7px 7px;
                                padding:5px 12px 9px; margin-bottom:10px;">
                        <a href="{creature['link']}" target="_blank" rel="noopener"
                           style="font-family:'Raleway',sans-serif; font-size:0.68rem;
                                  color:#40916c; text-decoration:none;
                                  border-bottom:1px solid rgba(64,145,108,0.3);
                                  padding-bottom:1px;">
                            ↗ Learn more
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # — Footer —
    st.markdown(
        """
        <div style="border-top:1px solid rgba(201,162,39,0.15); margin-top:20px;
                    padding:14px 0 8px; text-align:center;">
            <div style="font-family:'Raleway',sans-serif; font-size:0.6rem;
                        color:#4a3820; letter-spacing:0.05em;">
                Powered by LlamaIndex · Groq · Streamlit
            </div>
            <div style="font-family:'Raleway',sans-serif; font-size:0.58rem;
                        color:#3a2d1a; margin-top:3px;">
                © DreamWorks Animation 2026 — Forgotten Island
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main area — header banner
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding:36px 0 4px;">
        <div style="font-family:'Cinzel',serif; font-size:2.4rem; color:#c9a227;
                    text-shadow:0 0 35px rgba(201,162,39,0.4),
                                0 0 70px rgba(201,162,39,0.12);
                    letter-spacing:0.08em; line-height:1.2;">
            Forgotten Island
        </div>
        <div style="font-family:'Cinzel',serif; font-size:1.05rem; color:#40916c;
                    letter-spacing:0.22em; margin-top:7px;
                    text-shadow:0 0 14px rgba(64,145,108,0.5);">
            BATHALA-ALAM
        </div>
        <div style="font-family:'Raleway',sans-serif; font-size:0.82rem; color:#9a8060;
                    font-style:italic; margin-top:8px; letter-spacing:0.05em;">
            Guardian of Philippine Mythological Lore &nbsp;·&nbsp; Oracle of Nakali
        </div>
    </div>
    <div style="border-bottom:1px solid rgba(201,162,39,0.2);
                margin:18px auto 0; max-width:560px;"></div>
    <div style="text-align:center; margin:6px 0 20px;">
        <span style="font-family:'Raleway',sans-serif; font-size:0.65rem;
                     color:#4a3820; letter-spacing:0.12em;">
            ✦ &nbsp; A DREAMWORKS ANIMATION WORLD &nbsp; ✦
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# — Provider badge —
if st.session_state.use_openai:
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:10px;">
            <span style="font-family:'Raleway',sans-serif; font-size:0.68rem;
                         background:rgba(64,145,108,0.15); color:#40916c;
                         border:1px solid rgba(64,145,108,0.35); border-radius:20px;
                         padding:3px 12px; letter-spacing:0.06em;">
                ⚡ Backup Oracle Active &nbsp;·&nbsp; OpenAI gpt-4o-mini
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# — Engine error banner —
if st.session_state.engine_error:
    st.error(
        f"**The ancient spirits could not be awakened.**\n\n"
        f"{st.session_state.engine_error}\n\n"
        "Ensure your `GROQ_API_KEY` is set in `.streamlit/secrets.toml` "
        "(Streamlit Cloud) or in your `.env` file (local)."
    )

# ---------------------------------------------------------------------------
# Chat message history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🌿" if msg["role"] == "assistant" else "🔮"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ---------------------------------------------------------------------------
# Question handler (shared by sidebar buttons and chat input)
# ---------------------------------------------------------------------------
def _handle_question(question: str) -> None:
    """
    Displays the user message, queries the active engine, and appends the response.

    If the Groq engine raises a quota / rate-limit error and we haven't already
    switched, the function automatically rebuilds the engine with OpenAI
    (gpt-4o-mini) and retries — all within the same response turn.
    """
    from src.model_loader import is_quota_error

    # Show and store user turn
    with st.chat_message("user", avatar="🔮"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Generate and show assistant response
    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("☽  Consulting the sacred texts of Nakali..."):
            try:
                response = st.session_state.chat_engine.chat(question)
                response_text = str(response)

            except Exception as primary_exc:
                # --- Auto-fallback to OpenAI ---
                if not st.session_state.use_openai and is_quota_error(primary_exc):
                    st.toast(
                        "Primary oracle at capacity. Switching to backup oracle (OpenAI)...",
                        icon="⚡",
                    )
                    try:
                        st.session_state.use_openai = True
                        st.session_state.chat_engine = _build_session_engine(use_openai=True)
                        response = st.session_state.chat_engine.chat(question)
                        response_text = str(response)
                    except Exception as fallback_exc:
                        st.session_state.use_openai = False  # reset so badge doesn't show
                        response_text = (
                            "*Both oracles are unavailable at this time.*\n\n"
                            f"Groq error: `{primary_exc}`\n\n"
                            f"OpenAI error: `{fallback_exc}`\n\n"
                            "Please check your API keys or try again later."
                        )
                else:
                    # Non-quota error — surface it directly
                    response_text = (
                        f"*The spirits are unsettled: {primary_exc}*\n\n"
                        "Please try rephrasing your question."
                    )

        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})


# ---------------------------------------------------------------------------
# Process sidebar "Ask about X" button click
# ---------------------------------------------------------------------------
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    if _ensure_engine():
        _handle_question(question)

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if not st.session_state.engine_error:
    if prompt := st.chat_input(
        "Ask about creatures, diwata, the world of Nakali, or the Forgotten Island...",
    ):
        _handle_question(prompt)
