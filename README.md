# 🎓 The Rulebook That Argues With Itself

> A precision-engineered RAG (Retrieval-Augmented Generation) advisor built for university academic regulations (modeled on **SGSITS Indore**). It provides traceable, passage-grounded answers, admits ignorance on unmentioned queries, and explicitly flags contradictions when institutional regulations conflict across documents.

---

## 🌟 Core Highlights

The system operates across three deterministic, mutually exclusive states:
1. 🟢 **`ANSWERED`**: Authoritative answers verified with verbatim citations, section numbers, and exact line/page references.
2. ⚪ **`UNANSWERED`**: Polite, firm ignorance admission for plausible near-misses (e.g., family bereavement, visa delays, dress codes, lecture recording). Zero hand-waving or external hallucinations.
3. 🟡 **`CONTRADICTORY`**: Incompatible clauses across regulations are detected and rendered side-by-side with exact statutory excerpts and legal conflict analysis.

---

## ⚖️ The 3 Planted Contradictions

| # | Conflict Topic | Source A | Source B | Dispute Nature |
|---|---|---|---|---|
| **C1** | **Medical Attendance for Exam Eligibility** | `regulations.md` §4.1 & §4.3 (75% standard; 10% max condonation, setting absolute minimum floor at **65%**) | `scholarship_policy.pdf` p.2 §3.4 (Explicitly grants exam eligibility with **60%** attendance on medical leave) | A student with 62% attendance is detained under general regulations but authorized to write exams under the scholarship policy. |
| **C2** | **Late Fee Payment Cutoff Window** | `fee_deadlines.csv` Row 2 & 5 (Window closes strictly on **31st October 2024** with "zero extension") | `regulations.md` §8.4 (Academic Committee empowered to extend late payment deadline to **15th November**) | Schedule table specifies a hard deadline, while regulatory text confers discretionary committee override. |
| **C3** | **CGPA for Annual Scholarship Renewal** | `scholarship_policy.pdf` p.3 §4.2 (Mandatory minimum **8.00 CGPA**; prohibits automatic waivers) | `regulations.md` §5.5 (Dean's Merit List at **7.50 CGPA** awards automatic annual scholarship renewal) | Two different regulatory authorities dictate contradictory renewal standards for a 7.80 CGPA student. |

All three contradictions are formally documented with exact quotes in [`contradictions.md`](contradictions.md).

---

## 📊 Multi-Format Corpus (>6,200 Words)

1. **Markdown (`corpus/regulations.md`)** — `4,514 words`  
   Academic ordinances for SGSITS Indore covering admissions, attendance, 10-point CGPA grading, exams, Turnitin plagiarism (15% limit), disciplinary actions, hostel residency, and appellate rights.
2. **CSV Schedule (`corpus/fee_deadlines.csv`)** — `413 words`  
   Structured schedule of tuition, hostel room rent (₹31,450), mess advance (₹16,500), caution deposits, exam fees, and late penalty windows.
3. **PDF Document (`corpus/scholarship_policy.pdf`)** — `1,278 words` (4 pages)  
   Official institutional scholarship ordinance governing merit awards, attendance covenants, renewal criteria, and appeals.

---

## 🧪 Benchmark Evaluation & Test Set

The project includes an automated scoring script (`eval.py`) that scores all **40 benchmark cases** without prose interpretation:
- **10 `ANSWERED`**: Factual queries with verified citations.
- **25 `UNANSWERED`**: Hard, plausible near-misses testing boundary rigor.
- **5 `CONTRADICTORY`**: Planted contradictions tested across conflicting documents.

### Running the Evaluation
```bash
python eval.py
```

### Machine-Readable Evaluation Report
```
====================================================================
                 FINAL EVALUATION SUMMARY
====================================================================
Category         | Pass     | Fail     | Total    | Accuracy  
--------------------------------------------------------------------
ANSWERED         | 10       | 0        | 10       |    100.0%
UNANSWERED       | 25       | 0        | 25       |    100.0%
CONTRADICTORY    | 5        | 0        | 5        |    100.0%
--------------------------------------------------------------------
OVERALL          | 40       | 0        | 40       |    100.0%
====================================================================
```

---

## 🚀 Quick Setup & Run

### 1. Clone the Repository
```bash
git clone https://github.com/SuyashGupta14/AcademicRulebook.git
cd AcademicRulebook
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set API Key
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

### 4. Re-Index Vector Database (Optional)
```bash
python -m src.ingest
```

### 5. Launch the Web Interface
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to interact with the system.

---

## 📽️ Demo Recording

A full session recording demonstrating all three states (`ANSWERED`, `UNANSWERED`, and `CONTRADICTORY`) with source inspector verification is available in [`demo.webp`](demo.webp).

---

## 🏛️ Institutional Model

Modeled after **Shri Govindram Seksaria Institute of Technology and Science (SGSITS)**, Indore — an autonomous institution established in 1952 affiliated with RGPV Bhopal.
