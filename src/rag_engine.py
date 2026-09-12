"""
Core RAG Engine for SGSITS Academic Rulebook.

Pipeline:
1. Receives student query
2. Retrieves top-k candidate chunks from ChromaDB
3. Builds prompt with verbatim excerpts and strict boundary rules
4. Calls Google Gemini (Gemini 2.5 Flash / Gemini 2.0 Flash) with structured JSON schema
5. Validates and returns AnswerResponse Pydantic model
"""

import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import chromadb
from google import genai
from google.genai import types

from src.models import AnswerResponse, Citation
from src.prompts import SYSTEM_INSTRUCTION, build_query_prompt

load_dotenv()


class RulebookRAGEngine:
    """End-to-end RAG Advisor for Academic Regulations."""

    def __init__(
        self,
        persist_dir: str = "chroma_db",
        collection_name: str = "academic_rulebook",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model_name = model_name or os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

        # Initialize ChromaDB persistent client
        if not os.path.exists(self.persist_dir):
            raise RuntimeError(
                f"ChromaDB store not found at '{self.persist_dir}'. Run 'python -m src.ingest' first."
            )

        self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
        except Exception as e:
            raise RuntimeError(
                f"Collection '{self.collection_name}' not found. Run 'python -m src.ingest' first."
            ) from e

        # Initialize Gemini Client if API key is provided
        if self.api_key:
            self.genai_client = genai.Client(api_key=self.api_key)
        else:
            self.genai_client = None

    def retrieve(self, query: str, top_k: int = 8) -> List[Dict[str, Any]]:
        """Retrieve top candidate passages from vector store."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        passages = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            for doc, meta in zip(docs, metas):
                passages.append({
                    "source_file": meta.get("source_file", "unknown"),
                    "section": meta.get("section", "unknown"),
                    "location": meta.get("location", "unknown"),
                    "text": doc
                })
        return passages

    def ask(self, question: str, top_k: int = 8) -> AnswerResponse:
        """Process student question through RAG pipeline and return structured AnswerResponse."""
        if not self.api_key or not self.genai_client:
            raise ValueError(
                "GOOGLE_API_KEY is not set. Please add your key to .env file or pass it to RulebookRAGEngine."
            )

        # 1. Retrieve relevant passages
        passages = self.retrieve(question, top_k=top_k)

        # 2. Build structured prompt
        user_prompt = build_query_prompt(question, passages)

        # 3. Call Gemini with guaranteed Pydantic schema and quota retry loop
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=AnswerResponse,
            temperature=0.0
        )

        max_retries = 4
        for attempt in range(max_retries):
            try:
                response = self.genai_client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=config
                )

                response_text = response.text.strip()
                parsed_data = json.loads(response_text)
                return AnswerResponse(**parsed_data)

            except Exception as e:
                err_str = str(e)
                if ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str) and attempt < max_retries - 1:
                    wait_time = 15 + (attempt * 10)
                    # Look for suggested retry delay in error message
                    import re
                    match = re.search(r"retry in ([\d\.]+)s", err_str)
                    if match:
                        wait_time = min(float(match.group(1)) + 2.0, 60.0)
                    print(f"\n[Rate Limit] 429 received. Waiting {wait_time:.1f}s before retry {attempt+1}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"Error querying Gemini model: {err_str}") from e


def ask_rulebook(question: str) -> AnswerResponse:
    """Convenience helper function to ask a single question."""
    engine = RulebookRAGEngine()
    return engine.ask(question)


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "What is the mandatory attendance percentage required for exams?"
    engine = RulebookRAGEngine()
    print(f"Querying: {q}")
    try:
        ans = engine.ask(q)
        print(json.dumps(ans.model_dump(), indent=2))
    except Exception as err:
        print(f"Notice: {err}")
