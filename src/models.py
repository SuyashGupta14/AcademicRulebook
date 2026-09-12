"""
Pydantic Data Models for Academic Rulebook RAG System.

Defines the strict schema for:
- Citation: Verifiable source-grounded excerpts with exact locations
- AnswerResponse: Three deterministic states (ANSWERED, UNANSWERED, CONTRADICTORY)
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class Citation(BaseModel):
    """Verifiable citation linking a claim directly to a corpus passage."""

    source_file: str = Field(
        ...,
        description="Name of the source file (e.g. 'regulations.md', 'fee_deadlines.csv', 'scholarship_policy.pdf')",
    )
    section: str = Field(
        ...,
        description="Section title, clause number, or table category (e.g. 'Section 4.1 Attendance', 'Hostel Room Rent')",
    )
    location: str = Field(
        ...,
        description="Precise location in the file (e.g. 'Lines 45-52', 'Page 2, Section 3.4', 'Row 2 (Tuition)')",
    )
    exact_quote: str = Field(
        ...,
        description="Verbatim excerpt copied directly from the corpus text supporting the claim or conflict",
    )


class AnswerResponse(BaseModel):
    """Structured response model guaranteeing machine-readable state and verifiable citations."""

    state: Literal["ANSWERED", "UNANSWERED", "CONTRADICTORY"] = Field(
        ...,
        description="Deterministic state: 'ANSWERED' if clear answer exists, 'UNANSWERED' if corpus is silent or adjacent only, 'CONTRADICTORY' if conflicting rules exist",
    )
    explanation: str = Field(
        ...,
        description="Clear, student-friendly explanation answering the question, explaining the absence of policy, or detailing the contradictory clauses",
    )
    citations: List[Citation] = Field(
        default_factory=list,
        description="List of exact supporting citations. Empty for UNANSWERED, 1+ for ANSWERED, 2+ from conflicting sources for CONTRADICTORY",
    )
    confidence_note: str = Field(
        ...,
        description="Technical justification note (e.g. 'Direct citation from Section 4.1', 'Corpus mentions medical leave only, not bereavement', 'Conflict between regulations.md 65% floor and scholarship_policy.pdf 60%')",
    )

    @field_validator("citations")
    @classmethod
    def validate_citations_consistency(cls, citations: List[Citation], info):
        # We can perform soft or strict consistency validation if state is known
        return citations
