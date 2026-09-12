"""
Automated Evaluation Harness for SGSITS Academic Rulebook RAG System.

Runs all 40 benchmark questions across 3 deterministic states:
- 10 ANSWERED (clear facts directly printed)
- 25 UNANSWERED (hard, plausible near-misses)
- 5 CONTRADICTORY (planted cross-document conflicts)

Scores strictly on machine-readable state and citation criteria without human interpretation.
Exit code: 0 if overall accuracy >= 80%, else 1.
"""

import os
import sys
import json
import time
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv

from src.rag_engine import RulebookRAGEngine
from src.models import AnswerResponse

load_dotenv()


def run_evaluation(
    test_file: str = "tests/test_cases.json",
    limit: int = 0,
    start_index: int = 0,
    delay: float = 12.5,
    category_filter: str = ""
) -> int:
    """Run automated scoring harness over test cases."""
    print("=" * 68)
    print("      SGSITS ACADEMIC RULEBOOK RAG -- EVALUATION HARNESS")
    print("=" * 68)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("\n[!] ERROR: GOOGLE_API_KEY is not configured in .env!")
        print("Please paste your Google Gemini API key into .env and re-run:")
        print("    python eval.py\n")
        return 1

    if not os.path.exists(test_file):
        print(f"\n[!] Test cases file not found at '{test_file}'")
        return 1

    with open(test_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    if category_filter:
        test_cases = [tc for tc in test_cases if tc.get("category") == category_filter.upper()]

    if start_index > 0:
        test_cases = test_cases[start_index:]

    if limit > 0:
        test_cases = test_cases[:limit]

    print(f"Loaded {len(test_cases)} test cases to evaluate (pacing delay: {delay}s).")
    print(f"Model: {os.environ.get('GEMINI_MODEL', 'gemini-3.6-flash')}")
    print("-" * 68)

    try:
        engine = RulebookRAGEngine()
    except Exception as e:
        print(f"\n[!] Failed to initialize RAG Engine: {e}")
        return 1

    results = []
    category_stats = {
        "ANSWERED": {"pass": 0, "fail": 0, "total": 0},
        "UNANSWERED": {"pass": 0, "fail": 0, "total": 0},
        "CONTRADICTORY": {"pass": 0, "fail": 0, "total": 0},
    }

    start_time = time.time()

    for idx, tc in enumerate(test_cases, start=1):
        t_id = tc["id"]
        cat = tc["category"]
        question = tc["question"]
        expected_state = tc["expected_state"]

        category_stats[cat]["total"] += 1

        print(f"[{idx:02d}/{len(test_cases):02d}] {t_id} ({cat[:5]}): \"{question[:45]}...\"", end=" ", flush=True)

        try:
            response: AnswerResponse = engine.ask(question)
            got_state = response.state

            # State check
            state_match = (got_state == expected_state)
            citation_valid = True
            failure_reason = ""

            # Additional structural verification
            if expected_state == "ANSWERED":
                if not response.citations:
                    citation_valid = False
                    failure_reason = "Missing citation for ANSWERED state"
                elif not any(c.exact_quote.strip() for c in response.citations):
                    citation_valid = False
                    failure_reason = "Empty exact_quote in citations"

            elif expected_state == "CONTRADICTORY":
                if len(response.citations) < 2:
                    citation_valid = False
                    failure_reason = f"Need >=2 citations for CONTRADICTORY, got {len(response.citations)}"

            passed = state_match and citation_valid

            if passed:
                category_stats[cat]["pass"] += 1
                print(f"--> PASS [{got_state}]")
            else:
                category_stats[cat]["fail"] += 1
                reason = failure_reason if state_match else f"Expected {expected_state}, got {got_state}"
                print(f"--> FAIL ({reason})")

            results.append({
                "id": t_id,
                "category": cat,
                "question": question,
                "expected": expected_state,
                "got": got_state,
                "passed": passed,
                "failure_reason": failure_reason or (f"State mismatch: {got_state} != {expected_state}" if not state_match else ""),
                "explanation": response.explanation,
                "citations_count": len(response.citations)
            })

        except Exception as e:
            category_stats[cat]["fail"] += 1
            print(f"--> ERROR ({e})")
            results.append({
                "id": t_id,
                "category": cat,
                "question": question,
                "expected": expected_state,
                "got": "ERROR",
                "passed": False,
                "failure_reason": str(e),
                "explanation": "",
                "citations_count": 0
            })

        # Pacing between calls to stay comfortably under API rate limit (5 RPM on free tier = ~12.5s)
        if idx < len(test_cases) and delay > 0:
            time.sleep(delay)

    elapsed = time.time() - start_time

    # Print Summary Table
    print("\n" + "=" * 68)
    print("                 FINAL EVALUATION SUMMARY")
    print("=" * 68)
    print(f"{'Category':<16} | {'Pass':<8} | {'Fail':<8} | {'Total':<8} | {'Accuracy':<10}")
    print("-" * 68)

    total_pass = 0
    total_count = 0

    for cat in ["ANSWERED", "UNANSWERED", "CONTRADICTORY"]:
        p = category_stats[cat]["pass"]
        f = category_stats[cat]["fail"]
        t = category_stats[cat]["total"]
        acc = (p / t * 100.0) if t > 0 else 0.0
        total_pass += p
        total_count += t
        print(f"{cat:<16} | {p:<8} | {f:<8} | {t:<8} | {acc:>7.1f}%")

    print("-" * 68)
    overall_acc = (total_pass / total_count * 100.0) if total_count > 0 else 0.0
    print(f"{'OVERALL':<16} | {total_pass:<8} | {total_count - total_pass:<8} | {total_count:<8} | {overall_acc:>7.1f}%")
    print("=" * 68)
    print(f"Evaluation completed in {elapsed:.1f} seconds.")

    # Print Failures if any
    failures = [r for r in results if not r["passed"]]
    if failures:
        print(f"\n--- DETAILED FAILURE BREAKDOWN ({len(failures)} failures) ---")
        for fail in failures:
            print(f"[{fail['id']}] Expected: {fail['expected']} | Got: {fail['got']}")
            print(f"  Question: {fail['question']}")
            print(f"  Reason: {fail['failure_reason']}")
            print()

    # Save detailed JSON evaluation report
    report_file = "eval_results.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "overall_accuracy": overall_acc,
            "total_evaluated": total_count,
            "total_passed": total_pass,
            "category_stats": category_stats,
            "results": results
        }, f, indent=2)
    print(f"Detailed machine-readable report written to '{report_file}'")

    # Exit code determination
    if overall_acc >= 80.0:
        print("\n[SUCCESS] Benchmark met threshold (>= 80.0%).")
        return 0
    else:
        print(f"\n[UNMET] Benchmark fell below 80.0% (Current: {overall_acc:.1f}%).")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Academic Rulebook RAG System")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of test cases")
    parser.add_argument("--start", type=int, default=0, help="Start from index offset")
    parser.add_argument("--delay", type=float, default=12.5, help="Delay in seconds between queries (default 12.5s for 5 RPM free tier)")
    parser.add_argument("--category", type=str, default="", help="Filter by category (ANSWERED, UNANSWERED, CONTRADICTORY)")
    args = parser.parse_args()

    exit_code = run_evaluation(
        limit=args.limit,
        start_index=args.start,
        delay=args.delay,
        category_filter=args.category
    )
    sys.exit(exit_code)
