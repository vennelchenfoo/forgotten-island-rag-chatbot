# 🌊 Bathala-Alam — Philippine Mythology RAG Chatbot

*"Hindi ka nag-iisa. The old stories are still here — you just have to know how to ask."*

This project is more than a chatbot — it's a doorway into a world of Philippine mythological creatures that have lived in bedtime stories, bayanihan circles, and whispered warnings for centuries. And soon, for the first time, they will take center stage on the global screen in DreamWorks Animation's **Forgotten Island** — a 2026 film that brings Filipino folklore out of the barangay and into cinemas worldwide.

**Bathala-Alam** is an AI oracle trained on Philippine mythology. It speaks like your lolo or lola: grounded in knowledge, reverent of the old ways, and always ready with a story.

🔗 **[Try the live demo →](https://forgotten-island-bathala-alam.streamlit.app/)**

---

## 📖 The Story Behind the Bot

Growing up in the Philippines, creatures like the **Manananggal**, the **Tikbalang**, and the **Aswang** aren't just folklore — they are warnings, lessons, and guardians woven into the fabric of everyday life. Every province has its version. Every family has its story.

When DreamWorks announced *Forgotten Island*, something stirred. Here were characters that millions of Filipinos know intimately, but that the rest of the world was about to meet for the first time. It felt like a responsibility — and an opportunity.

I wanted to build something that could help people truly understand these beings. Not just their names, but their powers, their weaknesses, their regional variants, and the centuries of meaning behind them. Whether you're a Filipino reconnecting with your roots, a curious moviegoer preparing for the film, or simply someone who stumbled across the Aswang at 2am — this bot is for you.

This project was also my capstone at WBS Coding School's Data Science & AI Bootcamp. Not built on a generic toy dataset, but on something that actually matters.

---

## 🤖 What is a RAG Chatbot? (For Beginners)

**RAG** stands for **Retrieval-Augmented Generation** — a mouthful, but the idea is simple.

Imagine you hired a very smart intern. They can speak and write beautifully (that's the AI language model), but they don't know anything about Philippine mythology. So before they answer any question, you hand them a specific folder of documents to read first (that's the *retrieval* part). They search through those documents, pull out the most relevant pieces, and use *only* that information to write their answer.

This is better than asking an AI directly because:
- Answers are grounded in your actual source material, not guesswork
- The AI is far less likely to "hallucinate" (make things up)
- Every answer can be traced back to a source

The documents in this case? A carefully crafted mythology knowledge base covering **40+ Philippine creatures** across 8 mythological categories.

---

## 🏺 Creatures You Can Ask About

| Category | Examples |
|---|---|
| Shape-shifters & Predators | Aswang, Manananggal, Wak-Wak |
| Tricksters & Guardians | Tikbalang, Kapre, Nuno sa Punso |
| Water & Sea Spirits | Bakunawa, Siyokoy, Sirena |
| Nature Deities | Maria Makiling, Magwayen |
| Sky Beings | Amihan, Habagat |
| Undead | Multo, Bangungot |
| Mythical Animals | Sarimanok, Adarna |

---

## 🛠 Technical Approach

### The Pipeline at a Glance

```
User Question
    ↓
[1] Query Rewriting  →  translate casual language into document-language
    ↓
[2] Vector Search    →  find the 10 most relevant text chunks
    ↓
[3] Reranking        →  keep only the 2 best chunks
    ↓
[4] Memory           →  remember what was said earlier in the conversation
    ↓
[5] LLM Generation   →  answer as Bathala-Alam, grounded in retrieved context
```

---

### Chunking Strategy — How the Knowledge Was Split

Before the AI can search through documents, the text needs to be broken into manageable pieces called **chunks**. The challenge: too small, and you lose context. Too large, and you introduce noise.

Three configurations were tested and evaluated systematically:

| Chunk Size | Overlap | Outcome |
|---|---|---|
| 512 tokens | 50 tokens | Too narrow — missed important surrounding context |
| **768 tokens** | **115 tokens** | ✅ Best balance of coherence and precision |
| 1024 tokens | 200 tokens | Too broad — retrieval became unfocused |

**Winner: 768 tokens with 115 token overlap (≈15%).** Large enough to capture a full creature entry with context. Small enough that the search stays sharp.

---

### Reranking — Quality Over Quantity

After vector search returns 10 candidate chunks, a second, more precise model re-scores them for relevance. Think of it as a shortlist interview: the recruiter (vector search) finds 10 candidates, and the hiring manager (reranker) narrows it to the 2 best.

| Top-K Retrieved | Reranker Kept | Avg. Answer Correctness |
|---|---|---|
| 10 | **2** | **0.72** ✅ |
| 10 | 5 | 0.64 |
| 20 | 5 | 0.61 |

Counter-intuitive insight: **fewer, higher-quality chunks outperformed more chunks.** When you give the LLM too many candidates, it loses focus. Quality beats quantity — every time.

---

### Query Rewriting (HyDE) — Speaking the Same Language as the Documents

Source documents are written in formal, encyclopedic language. Users ask questions in casual human language. That gap can quietly hurt retrieval.

**HyDE (Hypothetical Document Embeddings)** bridges this: before searching, the AI generates a *hypothetical answer* in the same formal register as the source documents, then uses that to search. It's like translating your question into the language of the archive before you walk in.

Results: consistent ~3-5% improvement in answer correctness on complex questions. Small, but reliable. Worth keeping.

---

### Evaluation — Measuring What Actually Matters

Every optimization was measured using **RAGAS**, a framework built specifically for RAG systems. Four metrics tracked across all experiments:

| Metric | What It Checks |
|---|---|
| **Faithfulness** | Does the answer stay within what the retrieved context actually says? |
| **Answer Correctness** | Does the answer match the ground truth? |
| **Context Precision** | Are the retrieved chunks genuinely relevant to the question? |
| **Context Recall** | Did we retrieve all the information needed to answer well? |

Evaluation ran across **8 hand-crafted question-answer pairs** — from *"What are the Manananggal's weaknesses?"* to *"What are the five aspects of the Aswang?"* — progressing through four stages: baseline → chunking → reranking → query rewriting.

**Key findings:**
- The optimized pipeline (768/115 chunks + reranker 10→2 + HyDE) achieved **average answer correctness of ~0.72**, compared to lower scores at each prior stage
- Simple factual questions (Maria Makiling's domain, Manananggal weaknesses) scored highest — **0.72–0.78**
- The most complex question — linking mythology to the *Forgotten Island* film — scored the lowest (**0.52**), because it requires cross-referencing lore with film narrative rather than a direct lookup
- Every optimization was justified by the numbers, not by intuition

---

## ☁️ Deploying on Streamlit Free Tier

Streamlit Community Cloud is free — which is wonderful. The catch: **1 GB of RAM.** That sounds like a lot until you start loading AI models.

Here's what the original plan looked like vs. what actually made it to production:

| Component | What I Wanted | What Actually Fits in 1 GB |
|---|---|---|
| Embeddings | BAAI/bge-large-en (~1.3 GB) | OpenAI `text-embedding-3-small` — 0 MB local |
| Reranker | BAAI/bge-reranker-base (~278 MB) | `cross-encoder/ms-marco-MiniLM-L-6-v2` (~84 MB) |
| LLM | Any local model | Groq API (`llama-3.3-70b`) + OpenAI GPT-4o-mini fallback |

**Final memory footprint: ~544 MB** — well within the ceiling.

The strategy was: **use APIs for the heavy lifting, keep only what's necessary local.** The language model never runs on the server. Embeddings live in the cloud. Only the lightweight reranker loads locally.

One more wrinkle: Groq's free tier has daily token limits. When the bot gets popular (or I'm testing too enthusiastically), it hits the ceiling. The solution: an automatic fallback to OpenAI's API — seamless for users, painless for me.

---

## 🔧 Tech Stack

- **LLM**: Groq API (`llama-3.3-70b-versatile`) with OpenAI GPT-4o-mini fallback
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2` (HuggingFace)
- **RAG Framework**: LlamaIndex
- **Evaluation**: RAGAS
- **Frontend**: Streamlit
- **Knowledge Base**: Custom markdown mythology corpus (812 lines, 40+ creatures)

---

## 📂 Repository Structure

```
├── streamlit_app.py          # Main Streamlit application
├── main.py                   # CLI entry point for local testing
├── evaluate.py               # Evaluation pipeline orchestrator
├── src/                      # Core RAG engine, config, model loader
├── evaluation/               # RAGAS evaluation logic and results (CSV)
├── data/                     # Philippine mythology knowledge base
├── notebooks/                # 8 development and experimentation notebooks
├── images/                   # App screenshots
└── local_storage/            # Cached vector indices
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/vennelchenfoo/forgotten-island-rag-chatbot.git
cd forgotten-island-rag-chatbot
pip install -r requirements.txt
```

Add your API keys to a `.env` file:
```
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```

Run in the terminal:
```bash
python main.py
```

Or launch the full Streamlit app:
```bash
streamlit run streamlit_app.py
```

---

## 🎓 Key Learnings

- **Evaluation-driven design is not optional.** Every intuition I had about what "should" work better was wrong at least once. Numbers don't lie; feelings about chunk sizes do.
- **Free-tier constraints force good engineering.** Not having unlimited RAM pushed me toward lighter alternatives that, in several cases, performed just as well as the heavier ones.
- **The retrieval step matters as much as the LLM.** A brilliant language model giving wrong answers because it retrieved the wrong chunks is still a broken system.
- **Domain specificity is a superpower.** General-purpose AI knows about Philippine mythology vaguely. This bot knows it deeply — and that precision is exactly the point.

---

## 💡 Personal Reflections

This project is personal.

I grew up hearing stories about the Manananggal and the Aswang — half-fear, half-wonder, the way only childhood folklore can land. Building this bot was a way of honoring those stories. Of saying: *these characters deserve to be understood, not just feared.*

When *Forgotten Island* brings the Tikbalang and Bakunawa to a global audience, I want there to be a tool that helps people go deeper than the film credits. A place where the curiosity sparked by a cinema seat can become real knowledge about a culture that has been telling these stories for a thousand years.

This is that place.

---

*Built with curiosity, caffeine, and a deep respect for the old stories.*

*Vennel Chenfoo | Data Science & AI Bootcamp @ WBS Coding School*
*Career changer. Filipino. Building with data.*
