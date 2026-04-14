"""
TutasLearn — RAG Startup Knowledge Assistant
Streamlit UI
"""

import streamlit as st
from query_engine import ask_question

# ─── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="TutasLearn",
    page_icon="static/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM FONTS ──────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ─── DESIGN TOKENS (CSS variables) ─────────────────────────────
st.markdown("""
<style>
:root {
    --bg-primary: #0f0e0c;
    --bg-secondary: #1a1814;
    --bg-card: #211f1a;
    --bg-card-hover: #28251f;
    --bg-input: #161410;
    --border: #2e2b24;
    --border-light: #3d3a30;
    --text-primary: #f0e6d3;
    --text-secondary: #a89880;
    --text-muted: #6b6050;
    --accent: #d4a853;
    --accent-dim: #a07d3a;
    --accent-glow: rgba(212, 168, 83, 0.15);
    --accent-glow-strong: rgba(212, 168, 83, 0.25);
    --source-bg: #1c1a15;
    --tag-bg: rgba(212, 168, 83, 0.08);
    --tag-border: rgba(212, 168, 83, 0.25);
    --radius-card: 12px;
    --radius-tag: 999px;
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'Source Serif 4', Georgia, serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ── Reset & Base ── */
.stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-dim); }

/* ── Text selection ── */
::selection { background: var(--accent-glow-strong); color: var(--accent); }

/* ── Header ── */
.header-section {
    padding: 3.5rem 0 2rem;
    text-align: center;
    position: relative;
}

.header-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.2rem;
    opacity: 0;
    animation: fadeUp 0.6s ease 0.1s forwards;
}

.header-title {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.05;
    margin: 0 0 0.8rem;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.2s forwards;
}

.header-title em {
    font-style: italic;
    color: var(--accent);
}

.header-sub {
    font-family: var(--font-body);
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.35s forwards;
}

/* ── Divider ── */
.header-divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 2rem auto;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.45s forwards;
}

/* ── Search Box ── */
.search-wrapper {
    max-width: 700px;
    margin: 0 auto 1.5rem;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.5s forwards;
}

.search-container {
    position: relative;
    display: flex;
    align-items: center;
}

.search-icon {
    position: absolute;
    left: 1.4rem;
    color: var(--text-muted);
    pointer-events: none;
    z-index: 2;
    transition: color 0.3s;
}

.stTextInput > div > div > div:focus-within .search-icon,
.search-container:focus-within .search-icon {
    color: var(--accent);
}

.stTextInput > div > div {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-card) !important;
    padding: 0.2rem 0.5rem 0.2rem 0.2rem !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}

.stTextInput > div > div:focus-within {
    border-color: var(--accent-dim) !important;
    box-shadow: 0 0 0 3px var(--accent-glow), 0 0 20px var(--accent-glow) !important;
}

.stTextInput input {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 1.05rem !important;
    padding: 0.9rem 1rem 0.9rem 3.2rem !important;
    border: none !important;
    box-shadow: none !important;
}

.stTextInput input::placeholder {
    color: var(--text-muted) !important;
    font-style: italic;
}

.stButton > button {
    background: var(--accent) !important;
    color: #0f0e0c !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.7rem 1.4rem !important;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    white-space: nowrap;
}

.stButton > button:hover {
    background: #e0b86a !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(212, 168, 83, 0.35) !important;
}

.stButton > button:active {
    transform: translateY(0px);
}

/* ── Example questions ── */
.examples-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    justify-content: center;
    max-width: 700px;
    margin: 0 auto 3rem;
    opacity: 0;
    animation: fadeUp 0.7s ease 0.6s forwards;
}

.example-chip {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-secondary);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-tag);
    padding: 0.4rem 1rem;
    cursor: pointer;
    transition: all 0.25s ease;
    letter-spacing: 0.02em;
}

.example-chip:hover {
    color: var(--accent);
    border-color: var(--accent-dim);
    background: var(--tag-bg);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px var(--accent-glow);
}

/* ── Main content area ── */
.main-content {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 1.5rem 4rem;
}

/* ── Thinking indicator ── */
.thinking-container {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 1.2rem 1.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    margin-bottom: 1.5rem;
}

.thinking-label {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-dim);
}

.thinking-dots {
    display: flex;
    gap: 5px;
}

.thinking-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--accent-dim);
    animation: pulse-dot 1.4s ease-in-out infinite;
}

.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }

/* ── Answer Card ── */
.answer-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    overflow: hidden;
    margin-bottom: 1.5rem;
    animation: fadeUp 0.5s ease forwards;
}

.answer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
}

.answer-label {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
}

.answer-category-tag {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    background: var(--tag-bg);
    border: 1px solid var(--tag-border);
    border-radius: var(--radius-tag);
    padding: 0.25rem 0.75rem;
}

.answer-body {
    padding: 1.8rem 2rem;
    font-family: var(--font-body);
    font-size: 1.05rem;
    line-height: 1.85;
    color: var(--text-primary);
}

.answer-body p { margin: 0 0 1rem; }
.answer-body p:last-child { margin-bottom: 0; }

/* ── Sources Section ── */
.sources-section {
    border-top: 1px solid var(--border);
    padding: 1.2rem 1.5rem 1.5rem;
}

.sources-label {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.source-item {
    background: var(--source-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    transition: border-color 0.25s;
}

.source-item:last-child { margin-bottom: 0; }
.source-item:hover { border-color: var(--border-light); }

.source-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-bottom: 0.6rem;
}

.source-badge {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--accent);
    background: var(--tag-bg);
    border: 1px solid var(--tag-border);
    border-radius: var(--radius-tag);
    padding: 0.2rem 0.6rem;
}

.source-title {
    font-family: var(--font-body);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-primary);
    flex: 1;
}

.source-score {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
}

.source-excerpt {
    font-family: var(--font-body);
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.65;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.source-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
}

.source-tag {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius-tag);
    padding: 0.15rem 0.55rem;
}

/* ── Welcome / Empty state ── */
.welcome-card {
    text-align: center;
    padding: 3rem 2rem;
    animation: fadeUp 0.5s ease forwards;
}

.welcome-icon {
    font-size: 2.5rem;
    margin-bottom: 1.2rem;
    display: block;
}

.welcome-title {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 0.6rem;
}

.welcome-sub {
    font-family: var(--font-body);
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* ── Sidebar ── */
.stSidebar {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

.sidebar-section-title {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--accent) !important;
    margin-bottom: 0.8rem !important;
}

.sidebar-chip {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-secondary);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-tag);
    padding: 0.3rem 0.8rem;
    margin: 0.25rem 0.2rem;
    transition: all 0.2s;
}

.sidebar-chip:hover {
    color: var(--accent);
    border-color: var(--accent-dim);
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-dot {
    0%, 100% { opacity: 0.3; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

/* ── Streamlit overrides ── */
.stSpinner > div > div { border-top-color: var(--accent) !important; }

</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-section-title">📚 Knowledge Base</p>', unsafe_allow_html=True)

    categories = [
        "Product-Market Fit", "Product-User Fit", "Growth Strategy",
        "Lean Startup", "Startup Operations", "Case Study",
    ]
    for cat in categories:
        st.markdown(f'<span class="sidebar-chip">{cat}</span>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### About")
    st.markdown(
        "TutasLearn answers startup questions grounded in curated articles, "
        "case studies, and book summaries from top founders and investors."
    )
    st.markdown("**Model:** `llama3.2:1b` via Ollama")
    st.markdown("**Embedding:** `all-MiniLM-L6-v2`")

# ─── MAIN HEADER ────────────────────────────────────────────────
st.markdown("""
<div class="header-section">
    <div class="header-eyebrow">Startup Knowledge Assistant</div>
    <h1 class="header-title">Tutas<em>Learn</em></h1>
    <p class="header-sub">
        Ask anything about building a startup — powered by curated wisdom from
        Andreessen Horowitz, Y&nbsp;Combinator, Paul Graham, and Eric Ries.
    </p>
    <div class="header-divider"></div>
</div>
""", unsafe_allow_html=True)

# ─── SEARCH INPUT (Enter key submits via st.form) ────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# st.form with enter_to_submit=True: Enter key OR Ask button both submit
# clear_on_submit=True clears the text_input after submission
with st.form(key="search_form", clear_on_submit=True, enter_to_submit=True):
    col_query, col_btn = st.columns([1, 0.12], gap="small")
    with col_query:
        st.text_input(
            "search",
            placeholder="Ask about startups, product-market fit, growth strategy…",
            label_visibility="collapsed",
            key="main_query",
        )
    with col_btn:
        submitted = st.form_submit_button("Ask", use_container_width=True)

# Form submission triggers a re-run. st.session_state.main_query still holds
# the value at this point (before clear_on_submit takes effect on next render).
if submitted and st.session_state.main_query.strip():
    active_query = st.session_state.main_query.strip()
    

    st.session_state.messages.append({"role": "user", "content": active_query})

    with st.container():
        st.markdown("""
        <div class="thinking-container">
            <span class="thinking-label">Thinking</span>
            <div class="thinking-dots">
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    try:
        result = ask_question(active_query)
        primary_cat = "Startup"
        if result.get("sources"):
            meta = result["sources"][0].get("metadata", {})
            primary_cat = meta.get("category") or primary_cat
        result["category"] = primary_cat
        st.session_state.messages.append({"role": "assistant", "content": result})
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": {
                "answer": f"Something went wrong.\n\nError: {str(e)}",
                "sources": [],
                "category": "Error",
            }
        })

    st.rerun()

# ─── DISPLAY CHAT HISTORY ──────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="answer-card">
            <div class="answer-header">
                <span class="answer-label">You asked</span>
            </div>
            <div class="answer-body">
                <p>{msg['content']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        data = msg["content"]
        with st.container():
            st.markdown(f"""
            <div class="answer-card">
                <div class="answer-header">
                    <span class="answer-label">TutasLearn</span>
                    <span class="answer-category-tag">{data.get('category', 'Startup')}</span>
                </div>
                <div class="answer-body">
                    <p>{data['answer'].replace(chr(10), '<br>')}</p>
                </div>
                <div class="sources-section">
                    <div class="sources-label">📖 Sources &amp; References</div>
            """, unsafe_allow_html=True)

            for i, src in enumerate(data.get("sources", []), 1):
                meta = src.get("metadata", {})
                score = src.get("score")
                tags = meta.get("tags", "")
                tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

                st.markdown(f"""
                <div class="source-item">
                    <div class="source-meta">
                        <span class="source-badge">Source {i}</span>
                        <span class="source-title">{meta.get('title', 'Unknown')}</span>
                        <span class="source-score">score: {score}</span>
                    </div>
                    <div class="source-excerpt">{src.get('text', '')[:280]}…</div>
                    {''.join(f'<span class="source-tag">{t}</span>' for t in tag_list[:4]) if tag_list else ''}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)

# ─── WELCOME STATE ─────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <span class="welcome-icon">🧠</span>
        <h2 class="welcome-title">Ready to explore startup wisdom</h2>
        <p class="welcome-sub">
            Type your question above, or pick one of the suggested topics below.<br>
            Every answer includes citations to the original sources.
        </p>
    </div>
    """, unsafe_allow_html=True)
