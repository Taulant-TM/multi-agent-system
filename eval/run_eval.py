import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
import json
from agents.orchestrator import run_workflow

PASS_THRESHOLD = 0.7


def evaluate():
    with open("eval/test_questions.json", "r") as f:
        tests = json.load(f)

    results = []

    for test in tests:
        print(f"\nRunning: {test['task']}")

        result = run_workflow(test["task"])
        answer = result.get("final_answer", "").lower()

        contains_required = all(
            word.lower() in answer
            for word in test["must_contain"]
        )

        citation_check = True
        if test["must_have_citations"]:
            citation_check = "[" in answer and "]" in answer

        passed = contains_required and citation_check

        results.append({
            "task": test["task"],
            "passed": passed
        })

        print("PASS" if passed else "FAIL")

    total = len(results)
    passed_total = sum(r["passed"] for r in results)

    print("\n====== EVAL SUMMARY ======")
    print(f"Passed {passed_total}/{total}")

    return results


if __name__ == "__main__":
    evaluate()
