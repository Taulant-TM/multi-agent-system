from agents.orchestrator import run_workflow

result = run_workflow("Summarize project risks")
print(result["final_answer"])
print(result["trace"])