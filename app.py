"""
Streamlit Web Application: The Rulebook That Argues With Itself
A traceable, auditable RAG system for SGSITS Academic Regulations.
"""

import os
import time
import json
import streamlit as st
from dotenv import load_dotenv

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

# Custom CSS for rich, polished aesthetics (Dark mode, glassmorphism, vivid state badges)
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Polish */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
    }

    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* State Cards */
    .state-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .badge-answered {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-unanswered {
        background: rgba(148, 163, 184, 0.15);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }

    .badge-contradictory {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.45);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* Response Box */
    .response-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-top: 16px;
        margin-bottom: 20px;
    }

    .response-explanation {
        font-size: 1.05rem;
        line-height: 1.65;
        color: #F1F5F9;
        margin-bottom: 14px;
    }

    /* Citation Excerpt Card */
    .citation-card {
        background: rgba(30, 41, 59, 0.5);
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: 0.9rem;
    }

    .citation-source {
        font-weight: 600;
        color: #60A5FA;
        font-size: 0.82rem;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
    }

    .citation-quote {
        color: #E2E8F0;
        font-style: italic;
        line-height: 1.5;
        background: rgba(0, 0, 0, 0.25);
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 2px solid rgba(255, 255, 255, 0.2);
    }

    /* Contradiction Side-by-Side */
    .contra-box {
        background: rgba(245, 158, 11, 0.05);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 12px;
        padding: 16px;
        height: 100%;
    }

    .contra-header {
        font-weight: 700;
        color: #FBBF24;
        font-size: 0.88rem;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar — Configuration & Source Inspector
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/law.png", width=64)
    st.title("Rulebook Audit")
    st.caption("SGSITS Autonomous Regulations 2024–25")

    st.markdown("---")

    # API Key Handling
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
        st.success("API Key loaded from environment")

    # Model Selection
    model_choice = st.selectbox(
        "Gemini Reasoning Engine",
        ["gemini-3.6-flash", "gemini-2.5-pro", "gemini-flash-latest"],
        index=0
    )
    os.environ["GEMINI_MODEL"] = model_choice

    st.markdown("---")
    st.subheader("Corpus Statistics")
    st.markdown("""
    - **regulations.md**: `4,514 words`
    - **fee_deadlines.csv**: `413 words`
    - **scholarship_policy.pdf**: `1,278 words`
    - **Total Rulebook**: `6,205 words`
    - **Planted Contradictions**: `3 documented`
    """)

    st.markdown("---")
    st.caption("The Rulebook That Argues With Itself | Built for SGSITS Indore")


# Header / Hero
st.markdown("""
<div class="hero-card">
    <div class="hero-title">⚖️ The Rulebook That Argues With Itself</div>
    <div class="hero-subtitle">
        A deterministic, verifiable advisor for university academic regulations. Every answer is grounded in exact text passages, admits complete ignorance on unmentioned topics, and flags contradictory rules across institutional documents.
    </div>
</div>
""", unsafe_allow_html=True)

# Example Presets / Quick Questions
st.markdown("##### ⚡ Quick Demonstration Queries:")
c1, c2, c3, c4 = st.columns(4)

preset_query = None
with c1:
    if st.button("🟡 Medical Attendance Conflict", use_container_width=True, help="Tests planted contradiction C1 (65% vs 60%)"):
        preset_query = "What is the minimum attendance threshold for a medically exempted student to sit for exams?"
with c2:
    if st.button("🟡 Late Fee Window Conflict", use_container_width=True, help="Tests planted contradiction C2 (Oct 31 vs Nov 15)"):
        preset_query = "Can a student pay semester fees with a late fee after 31st October, or is that date strictly final?"
with c3:
    if st.button("⚪ Family Wedding / Bereavement", use_container_width=True, help="Tests near-miss UNANSWERED rejection"):
        preset_query = "Can I defer my mid-semester exam if an immediate family member passes away?"
with c4:
    if st.button("🟢 Standard Exam Attendance", use_container_width=True, help="Tests direct ANSWERED state (75% rule)"):
        preset_query = "What is the mandatory attendance percentage required to appear in the End-Semester Examination?"

# Query Input Box
query_input = st.text_input(
    "Ask any question about SGSITS academic regulations, attendance, fees, or scholarships:",
    value=preset_query or "",
    placeholder="e.g. Can I appear for examinations with 62% attendance if I have a hospital certificate?",
    key="query_box"
)

col_btn, col_info = st.columns([1, 4])
with col_btn:
    submit_btn = st.button("Audit Regulations", type="primary", use_container_width=True)

# Processing Logic
if submit_btn and query_input.strip():
    current_key = os.environ.get("GOOGLE_API_KEY", "")
    if not current_key or current_key == "your_gemini_api_key_here":
        st.error("⚠️ Please configure your **GOOGLE_API_KEY** in the sidebar or in your `.env` file.")
    else:
        with st.spinner("Retrieving clauses and auditing against rulebook..."):
            try:
                engine = RulebookRAGEngine()
                start_t = time.time()
                response: AnswerResponse = engine.ask(query_input.strip())
                latency = time.time() - start_t

                # Display Results based on State
                st.markdown("### Audit Finding")

                if response.state == "ANSWERED":
                    st.markdown("""
                    <div class="state-badge badge-answered">
                        🟢 State: ANSWERED
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="response-card">
                        <div class="response-explanation">{response.explanation}</div>
                        <div style="font-size:0.85rem; color:#94A3B8;">
                            <strong>Audit Justification:</strong> {response.confidence_note} &nbsp;•&nbsp; 
                            <em>Latency: {latency:.2f}s</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### 📜 Verifiable Citations")
                    for cit in response.citations:
                        st.markdown(f"""
                        <div class="citation-card">
                            <div class="citation-source">
                                <span>📄 {cit.source_file} &nbsp;|&nbsp; {cit.section}</span>
                                <span>📍 {cit.location}</span>
                            </div>
                            <div class="citation-quote">"{cit.exact_quote}"</div>
                        </div>
                        """, unsafe_allow_html=True)

                elif response.state == "UNANSWERED":
                    st.markdown("""
                    <div class="state-badge badge-unanswered">
                        ⚪ State: UNANSWERED (Silent on this matter)
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="response-card" style="border-left: 4px solid #94A3B8;">
                        <div class="response-explanation">{response.explanation}</div>
                        <div style="font-size:0.85rem; color:#94A3B8;">
                            <strong>Audit Note:</strong> {response.confidence_note} &nbsp;•&nbsp; 
                            <em>The system explicitly refused to extrapolate beyond official passages.</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.info("💡 **Why UNANSWERED?** The rulebook contains no clause on this specific request. Adjacent topics (such as medical leave or standard fee dates) cannot be extrapolated without formal administrative decree.")

                elif response.state == "CONTRADICTORY":
                    st.markdown("""
                    <div class="state-badge badge-contradictory">
                        🟡 State: CONTRADICTORY (Incompatible Regulations Detected)
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="response-card" style="border-left: 4px solid #F59E0B; background: rgba(245, 158, 11, 0.05);">
                        <div class="response-explanation">{response.explanation}</div>
                        <div style="font-size:0.85rem; color:#F59E0B;">
                            <strong>Conflict Audit:</strong> {response.confidence_note} &nbsp;•&nbsp;
                            <em>Latency: {latency:.2f}s</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### ⚔️ Conflicting Passages Comparison")
                    if len(response.citations) >= 2:
                        cols = st.columns(len(response.citations))
                        for idx, cit in enumerate(response.citations):
                            with cols[idx]:
                                st.markdown(f"""
                                <div class="contra-box">
                                    <div class="contra-header">Clause {idx+1}: {cit.source_file}</div>
                                    <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:6px;">
                                        <strong>Section:</strong> {cit.section}<br>
                                        <strong>Location:</strong> {cit.location}
                                    </div>
                                    <div class="citation-quote">"{cit.exact_quote}"</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        for cit in response.citations:
                            st.markdown(f"""
                            <div class="citation-card" style="border-left-color: #F59E0B;">
                                <div class="citation-source"><span>{cit.source_file} ({cit.location})</span></div>
                                <div class="citation-quote">"{cit.exact_quote}"</div>
                            </div>
                            """, unsafe_allow_html=True)

                # Expandable Source Inspector
                with st.expander("🔍 Inspect Raw Retrieved Passages from Vector Store"):
                    raw_passages = engine.retrieve(query_input.strip(), top_k=8)
                    for i, p in enumerate(raw_passages, 1):
                        st.markdown(f"**Passage #{i}** — `{p['source_file']}` | *{p['section']}* ({p['location']})")
                        st.code(p["text"], language="markdown")

            except Exception as e:
                st.error(f"Error executing RAG query: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem;">
    Shri G. S. Institute of Technology and Science, Indore (Autonomous 1952) • Academic Rulebook RAG System
</div>
""", unsafe_allow_html=True)
