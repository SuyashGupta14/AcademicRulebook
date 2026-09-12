# ⚖️ Formal Record of Planted Contradictions

This document records the exact locations, textual quotes, and legal conflict analysis for the three (3) intentional contradictions planted across the SGSITS Indore academic regulations corpus.

---

## Contradiction 1: Medical Attendance Threshold for End-Semester Exam Eligibility

- **Category**: Examination Eligibility vs. Medical Concession
- **Affected Parties**: Enrolled students seeking medical exemption to appear in examinations

### Clause A (General Academic Regulations)
- **Source File**: `corpus/regulations.md`
- **Section**: Section 4.1 & Section 4.3 ("Mandatory Attendance, Monitoring, and Condonation Protocols")
- **Exact Quote**:
  > *"Every registered candidate is statutorily required to attend a minimum of 75% of all scheduled lectures, tutorials, practical laboratory classes, and assigned departmental workshops in each enrolled subject individually to establish eligibility for appearing in the End-Semester Examination (ESE)... The Director of the Institute is vested with sole statutory discretion to condone an attendance deficiency of up to, but not exceeding, 10% (thereby establishing an absolute minimum attendance threshold of 65%) strictly on the grounds of acute hospitalization, severe incapacitating illness..."*
- **Legal Threshold Established**: **65% absolute minimum attendance floor** (75% standard minus maximum 10% condonation).

### Clause B (Scholarship Policy Ordinance)
- **Source File**: `corpus/scholarship_policy.pdf`
- **Section**: Page 2, Section 3.4 ("Medical Exemption & Examination Admissibility for Scholars")
- **Exact Quote**:
  > *"Notwithstanding any general academic ordinances, departmental circulars, or regulations published elsewhere in the Institute rulebook, scholarship recipients availing sanctioned medical leave under Section 3.3 shall be deemed legally eligible to appear for End-Semester Examinations provided their verified institutional attendance does not fall below sixty percent (60%) in the affected subjects."*
- **Legal Threshold Established**: **60% minimum attendance threshold** for medically exempted scholars.

### The Conflict
If a scholarship recipient undergoes verified inpatient medical treatment and finishes the semester with **62% attendance**:
- Under **`regulations.md` Section 4.3**, the student is below the absolute statutory minimum of 65%, receives a **'Z' grade**, and is detained from taking the exam.
- Under **`scholarship_policy.pdf` Section 3.4**, the student meets the 60% threshold and has an explicit statutory right to sit for the exam.
- Both provisions purport to have final governing authority over examination admissibility.

---

## Contradiction 2: Final Permissible Late Fee Payment Cutoff Date

- **Category**: Financial Deadlines & Institutional Discretion
- **Affected Parties**: All undergraduate, postgraduate, and hostel resident students remitting semester dues

### Clause A (Official Fee Schedule Table)
- **Source File**: `corpus/fee_deadlines.csv`
- **Rows**: Rows 2, 3, 4, 8, 9 ("Undergraduate Semester Tuition Fee", "Hostel Room Rent and Maintenance", etc.)
- **Exact Column Values**:
  - `Fee_Head`: Undergraduate Semester Tuition Fee / Hostel Room Rent
  - `Late_Fee_Window_Close`: `2024-10-31`
  - `Penalty_After_Final_Deadline`: *"Mandatory semester debarment and ERP credential deactivation; zero extension beyond 31st October"*
- **Legal Mandate Established**: **Firm cutoff on 31st October 2024** with zero extensions permitted under any circumstances.

### Clause B (Academic Regulations — Financial Governance)
- **Source File**: `corpus/regulations.md`
- **Section**: Section 8.4 ("Committee Authority on Late Fee Window Extension")
- **Exact Quote**:
  > *"Notwithstanding the standard published fee payment schedules and late penalty cutoff windows, the Academic Committee of the Institute, acting upon formal recommendation of the Dean of Academic Affairs, is empowered with full administrative discretion to extend the final permissible date for semester fee payment with late fee up to 15th November for the Autumn Semester upon consideration of demonstrated hardship, banking transit delays, or government scholarship distribution bottlenecks."*
- **Legal Mandate Established**: **Permissible extension up to 15th November 2024** at the discretion of the Academic Committee.

### The Conflict
Can a student tender fees with an applicable late penalty on **5th November 2024**?
- According to **`fee_deadlines.csv`**, the late fee window is permanently closed on 31st October with *"zero extension beyond 31st October"*, mandating debarment and ERP deactivation.
- According to **`regulations.md` Section 8.4**, the deadline is not final, and the Academic Committee possesses explicit legal authority to extend the late payment window to 15th November.

---

## Contradiction 3: CGPA Benchmark for Annual Merit Scholarship Renewal

- **Category**: Academic Honors vs. Scholarship Eligibility Standards
- **Affected Parties**: Meritorious students seeking continuation of their annual merit tuition waivers

### Clause A (Scholarship Policy Ordinance)
- **Source File**: `corpus/scholarship_policy.pdf`
- **Section**: Page 3, Section 4.2 ("Annual Renewal CGPA Benchmark")
- **Exact Quote**:
  > *"For all institutional merit, merit-cum-means, and endowment scholarships, annual renewal is strictly contingent upon maintaining a Cumulative Grade Point Average (CGPA) of not less than 8.00 (eight point zero zero) at the conclusion of each academic year, with zero uncleared backlogs (ATKT) across all preceding semesters. Any student whose cumulative CGPA falls below 8.00 at the end-of-year audit shall permanently forfeit their scholarship entitlement... no automatic waivers, honorary merit list exemptions, or external departmental provisions shall be honored or accepted to override this mandatory 8.00 CGPA standard."*
- **Legal Threshold Established**: **Mandatory minimum CGPA of 8.00**; explicit prohibition of external exemptions or honor roll waivers.

### Clause B (Academic Regulations — Grading & Honors)
- **Source File**: `corpus/regulations.md`
- **Section**: Section 5.5 ("Dean's Merit List & Scholarship Entitlement Clause")
- **Exact Quote**:
  > *"Students who maintain exemplary academic performance and achieve a CGPA of 7.50 or higher without any concurrent or historical backlogs at the close of an academic year shall be formally named to the Dean's Merit Honor Roll. Students holding Dean's Merit standing shall be entitled to automatic annual renewal of all institutional merit scholarships and fee waivers without being subjected to external review committees or separate application cycles."*
- **Legal Threshold Established**: **Automatic renewal triggered at CGPA of 7.50** for Dean's Merit Honor Roll awardees.

### The Conflict
Does a student with a **7.80 CGPA** qualify for scholarship renewal?
- Under **`regulations.md` Section 5.5**, having a CGPA ≥ 7.50 qualifies the student for the Dean's Merit Honor Roll, conferring an **automatic entitlement to annual scholarship renewal** without review.
- Under **`scholarship_policy.pdf` Section 4.2**, any student with a CGPA below 8.00 **permanently forfeits their scholarship**, with the text specifically stating that no "honorary merit list exemptions" can override the 8.00 benchmark.
