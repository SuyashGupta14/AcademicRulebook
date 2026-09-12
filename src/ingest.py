"""
Multi-format Ingestion Pipeline for SGSITS Academic Rulebook.

Parses:
1. Markdown: corpus/regulations.md (extracts sections with exact line ranges)
2. CSV: corpus/fee_deadlines.csv (extracts rows with column context)
3. PDF: corpus/scholarship_policy.pdf (extracts text per page with section references)

Chunks and indexes into persistent ChromaDB vector store.
"""

import os
import csv
import re
from typing import List, Dict, Any
import pdfplumber
import chromadb
from chromadb.config import Settings


def parse_markdown_corpus(file_path: str = "corpus/regulations.md") -> List[Dict[str, Any]]:
    """Parse markdown regulations, chunking by sections and tracking exact line numbers."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Regulations corpus not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks = []
    current_section = "General Regulations"
    current_lines = []
    start_line = 1

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Detect section headings
        if stripped.startswith("### Section") or stripped.startswith("## Section") or stripped.startswith("## "):
            # If we have accumulated lines, create a chunk
            if current_lines:
                chunk_text = "".join(current_lines).strip()
                if len(chunk_text) > 40:
                    chunks.append({
                        "source_file": "regulations.md",
                        "section": current_section,
                        "location": f"Lines {start_line}-{idx-1}",
                        "text": chunk_text
                    })
                current_lines = []

            current_section = stripped.lstrip("#").strip()
            start_line = idx

        current_lines.append(line)

        # If a section is very long (> 250 words), split into logical sub-chunks
        if len("".join(current_lines).split()) >= 280:
            chunk_text = "".join(current_lines).strip()
            chunks.append({
                "source_file": "regulations.md",
                "section": current_section,
                "location": f"Lines {start_line}-{idx}",
                "text": chunk_text
            })
            current_lines = []
            start_line = idx + 1

    # Remaining lines
    if current_lines:
        chunk_text = "".join(current_lines).strip()
        if len(chunk_text) > 40:
            chunks.append({
                "source_file": "regulations.md",
                "section": current_section,
                "location": f"Lines {start_line}-{len(lines)}",
                "text": chunk_text
            })

    return chunks


def parse_csv_corpus(file_path: str = "corpus/fee_deadlines.csv") -> List[Dict[str, Any]]:
    """Parse CSV fee schedule, formatting each row into a rich descriptive chunk."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fee schedule corpus not found at {file_path}")

    chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=2):
            category = row.get("Category", "General")
            fee_head = row.get("Fee_Head", "Fee")
            cohort = row.get("Target_Cohort", "Students")
            amount = row.get("Amount_INR", "0")
            due_date = row.get("Standard_Due_Date", "N/A")
            grace = row.get("Grace_Period_End", "N/A")
            late_fee = row.get("Late_Fee_INR", "N/A")
            close_date = row.get("Late_Fee_Window_Close", "N/A")
            penalty = row.get("Penalty_After_Final_Deadline", "N/A")
            authority = row.get("Governing_Authority", "Institute")

            text = (
                f"SGSITS Institutional Fee Schedule -- {category}: {fee_head}.\n"
                f"Target Cohort: {cohort}.\n"
                f"Amount: INR {amount}.\n"
                f"Standard Due Date: {due_date}. Grace Period End: {grace}.\n"
                f"Late Fee Surcharge: {late_fee}.\n"
                f"Final Late Fee Window Cutoff Date: {close_date}.\n"
                f"Penalty After Final Deadline: {penalty}.\n"
                f"Governing Statutory Authority: {authority}."
            )

            chunks.append({
                "source_file": "fee_deadlines.csv",
                "section": f"Fee Schedule -- {category}: {fee_head}",
                "location": f"Row {row_idx} ({fee_head})",
                "text": text
            })

    return chunks


def parse_pdf_corpus(file_path: str = "corpus/scholarship_policy.pdf") -> List[Dict[str, Any]]:
    """Parse PDF scholarship policy using pdfplumber, extracting per page and major section."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Scholarship PDF not found at {file_path}")

    chunks = []
    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            # Split page text into major subsections or paragraphs
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
            if not paragraphs:
                paragraphs = [text.strip()]

            for p_idx, para in enumerate(paragraphs, start=1):
                # Attempt to find section title if present
                first_line = para.split("\n")[0]
                section_title = first_line[:60] if len(first_line) > 5 else f"Scholarship Policy Page {page_idx}"

                chunks.append({
                    "source_file": "scholarship_policy.pdf",
                    "section": section_title,
                    "location": f"Page {page_idx}, Paragraph {p_idx}",
                    "text": para
                })

    return chunks


def ingest_all(
    persist_dir: str = "chroma_db",
    collection_name: str = "academic_rulebook"
) -> int:
    """Ingest all corpus files into persistent ChromaDB."""
    print("Beginning multi-format document ingestion...")

    md_chunks = parse_markdown_corpus()
    print(f"Parsed {len(md_chunks)} chunks from regulations.md")

    csv_chunks = parse_csv_corpus()
    print(f"Parsed {len(csv_chunks)} chunks from fee_deadlines.csv")

    pdf_chunks = parse_pdf_corpus()
    print(f"Parsed {len(pdf_chunks)} chunks from scholarship_policy.pdf")

    all_chunks = md_chunks + csv_chunks + pdf_chunks
    print(f"Total corpus chunks to index: {len(all_chunks)}")

    # Initialize ChromaDB persistent client
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_dir)

    # Recreate collection cleanly
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "SGSITS Academic Rulebook Corpus with Planted Contradictions"}
    )

    documents = [c["text"] for c in all_chunks]
    metadatas = [
        {
            "source_file": c["source_file"],
            "section": c["section"],
            "location": c["location"]
        }
        for c in all_chunks
    ]
    ids = [f"chunk_{i:04d}" for i in range(len(all_chunks))]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully ingested {len(all_chunks)} chunks into ChromaDB at '{persist_dir}'")
    return len(all_chunks)


if __name__ == "__main__":
    ingest_all()
