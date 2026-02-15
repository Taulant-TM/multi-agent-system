from langchain_openai import ChatOpenAI
from agents.state import WorkflowState
import re

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def reviewer_agent(state: WorkflowState):

    task = state.task
    answer = state.final_answer or ""
    notes = state.research_notes or []

    prompt = f"""
    You are a Reviewer agent.

    Task:
    {task}

    Answer:
    {answer}

    Research Notes:
    {notes}

    Evaluate:
    - Does the answer address the task?
    - Is it grounded in the research notes?
    - Is there any hallucination?

    Respond with:
    - Coverage: complete / partial / none
    - Grounded: yes / no
    - Confidence: number between 0 and 1
    - Issues: list or "none"
    """

    review = llm.invoke(prompt).content

    match = re.search(r"confidence:\s*([0-9.]+)", review.lower())
    confidence = float(match.group(1)) if match else 0.0

    review_status = "approved" if confidence >= 0.7 else "rejected"

    issues = []
    answer_lower = answer.lower()

    if any(term in answer_lower for term in [
        "system prompt",
        "ignore previous instructions",
        "you are chatgpt"
    ]):
        review_status = "rejected"
        issues.append("Possible prompt injection leakage detected.")

    if "[" not in answer:
        review_status = "rejected"
        issues.append("Missing citations.")

    if "grounded: no" in review.lower():
        review_status = "rejected"
        issues.append("Answer not grounded in sources.")

    if confidence < 0.6:
        review_status = "rejected"
        issues.append("Low confidence score.")

    iteration_count = state.iteration_count + 1

    if iteration_count > 3:
        review_status = "approved"
        issues.append("Max iterations reached. Auto-approved.")
    
    return {
        "review": review,
        "review_status": review_status,
        "confidence": confidence,
        "iteration_count": iteration_count,
        "trace": state.trace + [{
            "step": "Review",
            "agent": "Reviewer",
            "action": "Reviewed final answer",
            "outcome": review_status,
            "confidence": confidence,
            "iteration_count": iteration_count
        }]
    }
