"""
Streamlit Web Application: The Rulebook That Argues With Itself
A traceable, auditable RAG system for SGSITS Academic Regulations.
"""

import os
import time
import json
import warnings
import streamlit as st
from dotenv import load_dotenv

# Suppress harmless SDK notices
warnings.filterwarnings("ignore", category=UserWarning)

from src.rag_engine import RulebookRAGEngine
from src.models import AnswerResponse

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SGSITS Academic Rulebook Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: High-contrast, clean modern academic theme with vibrant state badges
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }

    /* Hero Card */
    .hero-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.2);
    }

    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        color: #E2E8F0 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* State Badges */
    .state-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .badge-answered {
        background: #DCFCE7 !important;
        color: #15803D !important;
        border: 1px solid #86EFAC;
    }

    .badge-unanswered {
        background: #F1F5F9 !important;
        color: #475569 !important;
        border: 1px solid #CBD5E1;
    }

    .badge-contradictory {
        background: #FEF3C7 !important;
        color: #B45309 !important;
        border: 1px solid #FCD34D;
        animation: pulse-border 2s infinite;
    }

    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
        70% { box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* Response Cards */
    .response-card {
        border-radius: 14px;
        padding: 22px;
        margin-top: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .response-card-answered {
        background: #F0FDF4 !important;
        border: 1.5px solid #86EFAC;
    }

    .response-card-unanswered {
        background: #F8FAFC !important;
        border: 1.5px solid #CBD5E1;
    }

    .response-card-contradictory {
        background: #FFFBEB !important;
        border: 1.5px solid #FCD34D;
    }

    .response-explanation {
        font-size: 1.05rem;
        line-height: 1.65;
        color: #0F172A !important;
        margin-bottom: 14px;
        font-weight: 500;
    }

    .response-meta {
        font-size: 0.85rem;
        color: #64748B !important;
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        padding-top: 10px;
    }

    /* Verifiable Citation Cards */
    .citation-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    }

    .citation-source {
        font-weight: 700;
        color: #1D4ED8 !important;
        font-size: 0.88rem;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .citation-location-badge {
        background: #EFF6FF;
        color: #1E40AF;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        border: 1px solid #BFDBFE;
    }

    .citation-quote {
        color: #1E293B !important;
        font-style: italic;
        line-height: 1.6;
        background: #F8FAFC;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 3px solid #3B82F6;
        font-size: 0.92rem;
    }

    /* Side-by-side Contradiction Comparison */
    .contra-card {
        background: #FFFFFF !important;
        border: 1.5px solid #F59E0B;
        border-radius: 12px;
        padding: 18px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.1);
    }

    .contra-header {
        font-weight: 700;
        color: #B45309 !important;
        font-size: 0.95rem;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .contra-meta {
        font-size: 0.82rem;
        color: #475569 !important;
        margin-bottom: 12px;
        line-height: 1.45;
    }

    .contra-quote {
        color: #1E293B !important;
        font-style: italic;
        line-height: 1.55;
        background: #FFFBEB;
        padding: 12px 14px;
        border-radius: 8px;
        border-left: 3px solid #D97706;
        font-size: 0.9rem;
    }

    /* Preset Quick Buttons */
    div[data-testid="stHorizontalBlock"] .stButton button {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 10px !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        padding: 8px 10px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }

    div[data-testid="stHorizontalBlock"] .stButton button:hover {
        border-color: #2563EB !important;
        color: #1D4ED8 !important;
        background: #EFF6FF !important;
    }

    /* Primary Action Button */
    button[kind="primary"] {
        background: #2563EB !important;
        border: 1px solid #1D4ED8 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }

    button[kind="primary"]:hover {
        background: #1D4ED8 !important;
    }

    /* ── Sidebar: Dark Premium Theme ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid #334155;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #E2E8F0 !important;
    }

    section[data-testid="stSidebar"] strong {
        color: #F1F5F9 !important;
    }

    section[data-testid="stSidebar"] code {
        color: #38BDF8 !important;
        background: rgba(56, 189, 248, 0.1) !important;
        padding: 2px 6px;
        border-radius: 4px;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #334155 !important;
        opacity: 0.6;
    }

    /* Sidebar cards */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        backdrop-filter: blur(8px);
    }

    .sidebar-card-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }

    /* Sidebar input/select overrides */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #1E293B !important;
        border: 1px solid #475569 !important;
        color: #F1F5F9 !important;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] .stSelectbox svg {
        fill: #94A3B8 !important;
    }

    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #1E293B !important;
        border: 1px solid #475569 !important;
        color: #F1F5F9 !important;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: #64748B !important;
    }

    /* Sidebar API Key active badge */
    .api-key-badge {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.35);
        padding: 8px 14px;
        border-radius: 8px;
        color: #4ADE80 !important;
        font-size: 0.85rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar caption */
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] caption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #64748B !important;
    }

    /* Sidebar collapse button */
    section[data-testid="stSidebar"] button[kind="header"] {
        color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""
if "trigger_search" not in st.session_state:
    st.session_state["trigger_search"] = False

# Sidebar — Configuration & Corpus Metrics
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0 16px 0;">
        <span style="font-size: 2.4rem;">⚖️</span>
        <div>
            <h2 style="margin: 0; font-size: 1.3rem; font-weight: 800; color: #FFFFFF !important;">Rulebook Audit</h2>
            <div style="font-size: 0.8rem; color: #94A3B8 !important; font-weight: 500;">SGSITS Regulations 2024–25</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Card 1: API Key & Model
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card-title">🔑 Configuration</div>', unsafe_allow_html=True)

    env_api_key = os.environ.get("GOOGLE_API_KEY", "")
    has_env_key = bool(env_api_key and env_api_key != "your_gemini_api_key_here")

    if not has_env_key:
        user_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your free API key at aistudio.google.com/apikey"
        )
        if user_api_key:
            os.environ["GOOGLE_API_KEY"] = user_api_key
            st.success("API Key activated!")
    else:
        st.markdown("""
        <div class="api-key-badge">
            <span>✓</span> API Key Active
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    model_choice = st.selectbox(
        "Gemini Reasoning Engine",
        ["gemini-flash-latest", "gemini-3.6-flash", "gemini-2.5-flash-lite"],
        index=0
    )
    os.environ["GEMINI_MODEL"] = model_choice

    st.markdown('</div>', unsafe_allow_html=True)

    # Card 2: Corpus Breakdown
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">📚 Corpus Breakdown</div>
        <div style="font-size: 0.88rem; line-height: 1.85; color: #CBD5E1 !important;">
            • <strong style="color: #F1F5F9 !important;">regulations.md</strong>: <code>4,514 words</code><br>
            • <strong style="color: #F1F5F9 !important;">fee_deadlines.csv</strong>: <code>413 words</code><br>
            • <strong style="color: #F1F5F9 !important;">scholarship_policy.pdf</strong>: <code>1,278 words</code><br>
        </div>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.08);">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px;">
                <span style="color: #94A3B8 !important;">Total Corpus</span>
                <strong style="color: #FFFFFF !important;">6,205 words</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px;">
                <span style="color: #94A3B8 !important;">Planted Contradictions</span>
                <code style="color: #FBBF24 !important; background: rgba(251, 191, 36, 0.1) !important;">3</code>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                <span style="color: #94A3B8 !important;">Test Benchmark</span>
                <code>40 cases</code>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    st.caption("Shri G. S. Institute of Technology & Science, Indore • Autonomous 1952")

# Main Hero
st.markdown("""
<div class="hero-card">
    <div class="hero-title">
        <span>⚖️</span>
        <span>The Rulebook That Argues With Itself</span>
    </div>
    <div class="hero-subtitle">
        A deterministic, verifiable advisor for university academic regulations. Every answer is grounded in exact text passages, admits complete ignorance on unmentioned topics, and flags contradictory rules across institutional documents.
    </div>
</div>
""", unsafe_allow_html=True)

# Preset demonstration buttons
st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #0F172A !important; margin-bottom: 8px;'>⚡ Quick Demonstration Queries:</div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

def set_query(text):
    st.session_state["query_input"] = text
    st.session_state["trigger_search"] = True

with c1:
    if st.button("🟡 Medical Attendance Conflict", use_container_width=True, help="Tests planted contradiction C1 (65% vs 60%)"):
        set_query("What is the minimum attendance threshold for a medically exempted student to sit for exams?")

with c2:
    if st.button("🟡 Late Fee Window Conflict", use_container_width=True, help="Tests planted contradiction C2 (Oct 31 vs Nov 15)"):
        set_query("Is the late fee payment cutoff strictly closed on 31st October with zero extensions permitted, or can late fees be accepted until 15th November?")

with c3:
    if st.button("⚪ Family Bereavement Absence", use_container_width=True, help="Tests near-miss UNANSWERED rejection"):
        set_query("Can I defer my mid-semester exam if an immediate family member passes away?")

with c4:
    if st.button("🟢 Standard Exam Attendance", use_container_width=True, help="Tests direct ANSWERED state (75% rule)"):
        set_query("What is the standard mandatory attendance percentage required for regular students to appear in the End-Semester Examination?")

# Query Input
query_input = st.text_input(
    "Ask any question about SGSITS academic regulations, attendance, fees, or scholarships:",
    value=st.session_state["query_input"],
    placeholder="e.g. Can I appear for examinations with 62% attendance if I have a hospital certificate?",
    key="text_search_box"
)

col_btn, col_spacer = st.columns([1, 4])
with col_btn:
    submit_btn = st.button("Audit Regulations", type="primary", use_container_width=True)

# Trigger if submitted manually or via preset
should_execute = submit_btn or st.session_state["trigger_search"]
# Reset trigger
st.session_state["trigger_search"] = False

active_query = query_input.strip() or st.session_state["query_input"].strip()

if should_execute and active_query:
    current_key = os.environ.get("GOOGLE_API_KEY", "")
    if not current_key or current_key == "your_gemini_api_key_here":
        st.error("⚠️ Please configure your **GOOGLE_API_KEY** in the sidebar or in your `.env` file.")
    else:
        with st.spinner("Retrieving clauses and auditing against rulebook..."):
            try:
                engine = RulebookRAGEngine()
                import time  # re-import locally to survive Streamlit re-runs
                start_t = time.time()
                response: AnswerResponse = engine.ask(active_query)
                latency = time.time() - start_t

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #0F172A !important;'>📋 Audit Findings</h3>", unsafe_allow_html=True)

                # State 1: ANSWERED
                if response.state == "ANSWERED":
                    st.markdown("""
                    <div class="state-badge badge-answered">
                        🟢 State: ANSWERED
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="response-card response-card-answered">
                        <div class="response-explanation">{response.explanation}</div>
                        <div class="response-meta">
                            <strong>Audit Note:</strong> {response.confidence_note} &nbsp;•&nbsp; 
                            <em>Audit Latency: {latency:.2f}s</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<h4 style='color: #0F172A !important;'>📜 Verifiable Citations</h4>", unsafe_allow_html=True)
                    for cit in response.citations:
                        st.markdown(f"""
                        <div class="citation-card">
                            <div class="citation-source">
                                <span>📄 {cit.source_file} &nbsp;•&nbsp; {cit.section}</span>
                                <span class="citation-location-badge">📍 {cit.location}</span>
                            </div>
                            <div class="citation-quote">"{cit.exact_quote}"</div>
                        </div>
                        """, unsafe_allow_html=True)

                # State 2: UNANSWERED
                elif response.state == "UNANSWERED":
                    st.markdown("""
                    <div class="state-badge badge-unanswered">
                        ⚪ State: UNANSWERED (Silent on this matter)
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="response-card response-card-unanswered">
                        <div class="response-explanation">{response.explanation}</div>
                        <div class="response-meta">
                            <strong>Audit Note:</strong> {response.confidence_note} &nbsp;•&nbsp; 
                            <em>The system explicitly refused to extrapolate beyond official passages.</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.info("💡 **Why UNANSWERED?** The rulebook contains no statutory provision for this specific inquiry. Adjacent policies (such as medical leave or fee schedules) cannot be assumed or conflated.")

                # State 3: CONTRADICTORY
                elif response.state == "CONTRADICTORY":
                    st.markdown("""
                    <div class="state-badge badge-contradictory">
                        🟡 State: CONTRADICTORY (Incompatible Regulations Detected)
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="response-card response-card-contradictory">
                        <div class="response-explanation" style="color: #78350F !important;">{response.explanation}</div>
                        <div class="response-meta" style="color: #92400E !important;">
                            <strong>Conflict Audit:</strong> {response.confidence_note} &nbsp;•&nbsp;
                            <em>Audit Latency: {latency:.2f}s</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<h4 style='color: #0F172A !important;'>⚔️ Conflicting Passages Comparison</h4>", unsafe_allow_html=True)
                    if len(response.citations) >= 2:
                        cols = st.columns(len(response.citations))
                        for idx, cit in enumerate(response.citations):
                            with cols[idx]:
                                st.markdown(f"""
                                <div class="contra-card">
                                    <div class="contra-header">
                                        <span>📌</span>
                                        <span>Clause {idx+1}: {cit.source_file}</span>
                                    </div>
                                    <div class="contra-meta">
                                        <strong>Section:</strong> {cit.section}<br>
                                        <strong>Location:</strong> {cit.location}
                                    </div>
                                    <div class="contra-quote">"{cit.exact_quote}"</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        for cit in response.citations:
                            st.markdown(f"""
                            <div class="citation-card" style="border-left-color: #D97706;">
                                <div class="citation-source">
                                    <span>📄 {cit.source_file} ({cit.section})</span>
                                    <span class="citation-location-badge">📍 {cit.location}</span>
                                </div>
                                <div class="citation-quote">"{cit.exact_quote}"</div>
                            </div>
                            """, unsafe_allow_html=True)

                # Source Inspector
                with st.expander("🔍 Inspect Raw Retrieved Passages from Vector Store"):
                    raw_passages = engine.retrieve(active_query, top_k=8)
                    for i, p in enumerate(raw_passages, 1):
                        st.markdown(f"**Passage #{i}** — `{p['source_file']}` | *{p['section']}* ({p['location']})")
                        st.code(p["text"], language="markdown")

            except Exception as e:
                st.error(f"Error executing RAG query: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding-top: 8px;">
    Shri G. S. Institute of Technology and Science, Indore (Autonomous 1952) • Academic Rulebook RAG System
</div>
""", unsafe_allow_html=True)
