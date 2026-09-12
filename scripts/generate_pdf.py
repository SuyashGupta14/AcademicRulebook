"""
Script to generate corpus/scholarship_policy.pdf using fpdf2.
Contains formal institutional scholarship ordinances,
including planted contradictions C1 (60% attendance threshold on medical exemption)
and C3 (8.00 CGPA renewal threshold).
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos


class ScholarshipPolicyPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(70, 70, 70)
        self.cell(
            0,
            8,
            "SHRI G. S. INSTITUTE OF TECHNOLOGY & SCIENCE (SGSITS) INDORE",
            border=0,
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self.set_font("Helvetica", "I", 8)
        self.cell(
            0,
            5,
            "Office of the Dean of Student Welfare | Institutional Scholarship Regulations (SGSITS-SCH-2024-V1)",
            border=0,
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self.ln(2)
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        page_str = f"Page {self.page_no()} of {{nb}}"
        self.cell(0, 10, page_str, align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(20, 40, 90)
        self.cell(0, 8, title, border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(40, 50, 70)
        self.cell(0, 6, title, border=0, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(3)


def build_pdf():
    os.makedirs("corpus", exist_ok=True)
    pdf = ScholarshipPolicyPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)

    # PAGE 1: Preamble, Objectives, Categorization & Eligibility
    pdf.add_page()
    pdf.chapter_title("OFFICIAL ORDINANCE ON INSTITUTIONAL SCHOLARSHIPS AND MERIT ENDOWMENTS")
    pdf.body_text(
        "Document Reference: SGSITS/DSW/SCHOLARSHIP/REG-2024/01\n"
        "Effective Date: 1st July 2024 | Approved by Governing Body Resolution GB-88/2024\n"
        "Supervising Statutory Officer: Dean of Student Welfare (DSW), SGSITS Indore"
    )

    pdf.section_title("1. Preamble and Policy Objectives")
    pdf.body_text(
        "1.1. Shri Govindram Seksaria Institute of Technology and Science, Indore, in recognition of academic excellence, "
        "social equity, and intellectual rigor, institutes this comprehensive Scholarship and Financial Assistance Policy. "
        "The fundamental mandate of this policy is to ensure that no meritorious student admitted to an undergraduate or "
        "postgraduate program is impeded from completing their professional education due to financial hardship.\n\n"
        "1.2. The provisions of this policy govern all institutional merit scholarships, alumni endowment stipends, "
        "industry-sponsored fellowships, fee waiver concessions, and special benevolent grants administered directly by the "
        "Institute Trust and the Dean of Student Welfare.\n\n"
        "1.3. External statutory welfare scholarships (such as Post-Matric SC/ST/OBC scholarships awarded by the Government "
        "of Madhya Pradesh or the National Scholarship Portal) shall be processed according to respective state government "
        "directives; however, institutional matching disbursements and top-up stipends shall remain strictly bound by this ordinance."
    )

    pdf.section_title("2. Classification of Institutional Scholarships and Award Amounts")
    pdf.body_text(
        "2.1. Category A -- Director's Diamond Jubilee Institute Merit Scholarship:\n"
        "Awarded to the top two (2) rank holders in each branch of engineering based on JEE Main ranks during admission year, "
        "and highest annual SGPA/CGPA in subsequent academic years. Disburses 100% full tuition fee waiver amounting to "
        "INR 95,000 per academic year plus an annual book grant of INR 10,000.\n\n"
        "2.2. Category B -- Seksaria Merit-Cum-Means (MCM) Endowment Grants:\n"
        "Awarded to students demonstrating cumulative family annual income below INR 3.50 Lakhs who obtain a minimum CGPA "
        "of 7.50 upon admission or annual evaluation. Disburses 50% tuition waiver (INR 47,500 per academic year).\n\n"
        "2.3. Category C -- Smt. Shantabai Seksaria Memorial Women in STEM Scholarship:\n"
        "Dedicated financial fellowship awarded to top-ranking female students in Computer Science, Information Technology, "
        "and Electronics Engineering, providing INR 50,000 annual scholarship allowance.\n\n"
        "2.4. Category D -- Postgraduate GATE Research Fellowships:\n"
        "Administered for regular AICTE-admitted M.Tech. scholars holding valid GATE scores, granting INR 12,400 monthly stipend "
        "for 24 months, subject to weekly 8-hour departmental teaching assistance duties."
    )

    # PAGE 2: Attendance Requirements & Planted Contradiction 1
    pdf.add_page()
    pdf.chapter_title("ATTENDANCE COVENANTS, MEDICAL EXEMPTIONS AND LEAVE RULES")

    pdf.section_title("3. Institutional Attendance Standards for Scholarship Holders")
    pdf.body_text(
        "3.1. General Attendance Obligation:\n"
        "Every scholarship beneficiary is obligated to maintain exemplary classroom, tutorial, and practical laboratory engagement. "
        "The standard expected attendance performance for all scholarship recipients is ninety percent (90%) in each registered subject.\n\n"
        "3.2. Routine Absence Limitations:\n"
        "Absence from classes without sanctioned leave of absence in excess of five (5) cumulative instructional days in a single "
        "calendar month shall lead to the immediate withholding of that month's scholarship stipend tranche.\n\n"
        "3.3. Sanction of Authorized Medical Leave:\n"
        "In the event of severe infectious illness, surgical intervention, or inpatient medical treatment, the scholarship "
        "recipient must submit a medical application accompanied by hospital discharge documentation countersigned by the "
        "Chief Medical Officer of Maharaja Yeshwantrao Hospital (MYH) Indore to the Dean of Student Welfare within ten (10) days."
    )

    pdf.section_title("3.4. Medical Exemption & Examination Admissibility for Scholars [PLANTED CONTRADICTION C1]")
    pdf.body_text(
        "Notwithstanding any general academic ordinances, departmental circulars, or regulations published elsewhere in the "
        "Institute rulebook, scholarship recipients availing sanctioned medical leave under Section 3.3 shall be deemed legally "
        "eligible to appear for End-Semester Examinations provided their verified institutional attendance does not fall below "
        "sixty percent (60%) in the affected subjects. "
        "The Scholarship Standing Committee affirms that a student holding institutional merit credentials who is incapacitated "
        "by authenticated medical circumstances shall not be detained from examination eligibility if they achieve the sixty "
        "percent (60%) threshold. This specific provision supersedes conflicting standard departmental attendance ceilings."
    )

    pdf.section_title("3.5. Procedure for Verifying Attendance Shortfalls")
    pdf.body_text(
        "Before publishing the final examination debarment roster, the Controller of Examinations must transmit a confidential "
        "list of all detained candidates to the Dean of Student Welfare. If any listed candidate is a certified scholarship "
        "recipient possessing valid medical leave certification exceeding forty percent shortfall, their attendance record shall "
        "be recalculated against the 60% medical baseline before debarment orders are executed."
    )

    # PAGE 3: Renewal Thresholds, Planted Contradiction 3, Revocation
    pdf.add_page()
    pdf.chapter_title("CRITERIA FOR ANNUAL RENEWAL AND MAINTENANCE OF AWARDS")

    pdf.section_title("4. Annual Performance Evaluation and Renewal Benchmarks")
    pdf.body_text(
        "4.1. Annual Review Cycle:\n"
        "Every scholarship awarded under this code is initially granted for a duration of one academic year (two consecutive "
        "instructional semesters). Continued disbursement in subsequent academic years is not unconstrained and requires rigorous "
        "formal re-evaluation by the Institutional Scholarship Scrutiny Board during the annual summer audit."
    )

    pdf.section_title("4.2. Annual Renewal CGPA Benchmark [PLANTED CONTRADICTION C3]")
    pdf.body_text(
        "For all institutional merit, merit-cum-means, and endowment scholarships, annual renewal is strictly contingent upon "
        "maintaining a Cumulative Grade Point Average (CGPA) of not less than 8.00 (eight point zero zero) at the conclusion of "
        "each academic year, with zero uncleared backlogs (ATKT) across all preceding semesters. "
        "Any student whose cumulative CGPA falls below 8.00 at the end-of-year audit shall permanently forfeit their scholarship "
        "entitlement. The Institutional Scholarship Scrutiny Board shall strictly enforce this 8.00 CGPA renewal threshold; "
        "no automatic waivers, honorary merit list exemptions, or external departmental provisions shall be honored or accepted "
        "to override this mandatory 8.00 CGPA standard."
    )

    pdf.section_title("4.3. Disciplinary Debarment and Forfeiture Triggers")
    pdf.body_text(
        "A scholarship awarded under any category shall be summarily revoked, and the recipient required to refund all disbursed "
        "funds, upon the occurrence of any of the following disciplinary infractions:\n"
        "(a) Any proven participation, complicity, or instigation of ragging under Section 10 of the Academic Regulations.\n"
        "(b) Conviction of academic malpractice, plagiarism exceeding fifteen percent (15%), or examination hall cheating.\n"
        "(c) Destruction of Institute property, laboratory equipment sabotage, or unauthorized eviction strikes in hostels.\n"
        "(d) Submission of fraudulent, forged, or altered income certificates or domicile declarations during application."
    )

    # PAGE 4: Application Procedure, Grievances, Committee Powers
    pdf.add_page()
    pdf.chapter_title("APPLICATION WORKFLOW, APPEALS AND COMMITTEE GOVERNANCE")

    pdf.section_title("5. Application Protocols and Documentation Requirements")
    pdf.body_text(
        "5.1. The Dean of Student Welfare shall publish the official scholarship notification on the Institute portal by "
        "the 1st of August each academic year. All eligible aspirants must complete online applications via the SGSITS ERP portal.\n\n"
        "5.2. Mandatory accompanying documentation includes: High school grade transcripts, JEE scorecards, previous year "
        "mark sheets, original income certificate issued by an Executive Magistrate or Tehsildar (for MCM applicants), active "
        "State Bank of India savings account passbook linked to Aadhaar, and a character endorsement certificate signed by the HOD.\n\n"
        "5.3. Defective, incomplete, or unverified applications submitted after the 31st of August deadline shall be rejected "
        "without administrative recourse."
    )

    pdf.section_title("6. Scholarship Appeals and Grievance Committee")
    pdf.body_text(
        "6.1. Any student aggrieved by a decision of the Scholarship Scrutiny Board regarding disqualification, non-renewal, "
        "or computation of CGPA may prefer an appeal before the Institutional Scholarship Appellate Tribunal within fourteen (14) "
        "calendar days of the declaration of award rosters.\n\n"
        "6.2. The Tribunal, chaired by the Director of SGSITS and comprising the Dean of Academic Affairs, Dean of Student Welfare, "
        "and Registrar, shall review the petition and pronounce its final determination within twenty-one (21) days. "
        "The decision of the Director shall be final and binding on all parties."
    )

    pdf.section_title("7. Residual Administrative Mandate")
    pdf.body_text(
        "The Governing Body of SGSITS retains the statutory authority to revise scholarship stipends, alter endowment funding "
        "allocations, or institute new financial assistance categories to meet evolving academic requirements and state mandates."
    )

    output_path = "corpus/scholarship_policy.pdf"
    pdf.output(output_path)
    print(f"Successfully generated {output_path}")


if __name__ == "__main__":
    build_pdf()
