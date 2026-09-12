# 🎓 The Rulebook That Argues With Itself

> A precision-engineered RAG (Retrieval-Augmented Generation) advisor built for university academic regulations (modeled on **SGSITS Indore**). It gives traceable, passage-grounded answers, admits ignorance on unmentioned queries, and explicitly flags contradictions when regulations conflict.

---

## 🚀 Key Features

1. **Three Deterministic States**: Every query lands unambiguously in exactly one state:
   - 🟢 `ANSWERED`: Direct, unambiguous answer supported by verbatim cited passages.
   - ⚪ `UNANSWERED`: The rulebook contains no relevant authority (no hallucinations or hand-waving).
   - 🟡 `CONTRADICTORY`: Conflicting clauses exist across documents. Both are cited side-by-side with an explanation of the dispute.
2. **Strict Verifiable Traceability**: Every claim points directly to the source file, section, line or page number, and verbatim excerpt.
3. **Multi-Format Corpus (>6,500 words)**:
   - Markdown (`regulations.md`) — Academic ordinances, attendance, exams, discipline, and committee powers.
   - CSV Table (`fee_deadlines.csv`) — Structured schedules for tuition, hostel, mess, and late penalty windows.
   - PDF Document (`scholarship_policy.pdf`) — Official scholarship eligibility, GPA maintenance, and medical exceptions.
4. **Machine-Scored Eval Harness**: Runs 40 benchmark questions (10 answerable, 25 near-miss unanswerable, 5 contradictions) with zero human ambiguity.
5. **Interactive UI**: Streamlit web interface with real-time status badges, side-by-side conflict comparisons, and an expandable Source Inspector.

---

## 🛠️ Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/SuyashGupta14/AcademicRulebook.git
cd AcademicRulebook
pip install -r requirements.txt
```

### 2. Configure API Key
Copy `.env.example` to `.env` and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### 3. Ingest Documents into Vector Store
```bash
python -m src.ingest
```

### 4. Run Automated Evaluation
```bash
python eval.py
```

### 5. Launch the Web Interface
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
AcademicRulebook/
├── corpus/
│   ├── regulations.md         # SGSITS academic regulations (~4,500 words)
│   ├── fee_deadlines.csv      # Fee schedules and penalty dates (~500 words)
│   └── scholarship_policy.pdf # Merit scholarship policy (~1,500 words)
├── src/
│   ├── __init__.py
│   ├── models.py              # Pydantic schema for citations & response states
│   ├── ingest.py              # Multi-format ingestion into ChromaDB
│   ├── prompts.py             # System prompt with strict state boundary rules
│   └── rag_engine.py          # Gemini 2.5 Flash query pipeline & structured output
├── tests/
│   └── test_cases.json        # 40 hard test cases (25 near-miss unanswerable)
├── scripts/
│   └── generate_pdf.py        # PDF generator for scholarship corpus
├── contradictions.md          # Formal documentation of the 3 planted contradictions
├── eval.py                    # Automated test & scoring harness
├── app.py                     # Streamlit frontend with source inspector
├── requirements.txt
└── README.md
```
