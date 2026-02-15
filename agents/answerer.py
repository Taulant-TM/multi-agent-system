from langchain_openai import ChatOpenAI
from agents.state import WorkflowState
# import re
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def answer_agent(state: WorkflowState):

    previous_review = state.review or ""
    task = state.task
    notes = state.research_notes or []

    notes = [
        n for n in notes
        if n.get("content") and n.get("source")
    ]

    citations = "\n\nSources:\n" + "\n".join(
    f"[{i}] {n['source']}"
    for i, n in enumerate(notes, 1)
    )

    if not notes:
        return {
            "final_answer": "Not found in the provided sources.",
            "trace": state.trace + [{
                "step": "Write",
                "agent": "Writer",
                "action": "No relevant notes",
                "outcome": "Returned not found"
            }]
        }

    notes_text = ""
    for i, n in enumerate(notes, 1):
        notes_text += (
            f"[{i}] {n['content']}\n"
            f"Source: {n['source']}\n\n"
        )

    prompt = f"""
You are a Writer agent.

Return ONLY valid JSON with the following structure:

{{
    "executive_summary": string,
    "client_email": string,
    "action_items": [string]
}}

Rules:
- If a section is not relevant to the task, return it as an empty string "" (or empty list for action_items).
- Do NOT invent placeholder values.
- Do NOT fabricate content just to fill fields.
- Use ONLY research notes.
- No markdown.
- No explanation.
- JSON only

TASK:
{task}

Research Notes:
{notes_text}

Review Feedback:
{previous_review}
    """

    answer = llm.invoke(prompt).content
    
    try:
        structured = json.loads(answer)
    except:
        structured = {
            "executive_summary": "",
            "client_email": "",
            "action_items": []
        }

    executive_summary = structured.get("executive_summary", "")
    client_email = structured.get("client_email", "")
    action_items = structured.get("action_items", [])
    
    def deduplicate_paragraphs(text: str) -> str:
        if not isinstance(text, str):
            return ""
        seen = set()
        deduped = []
        for para in text.split("\n\n"):
            stripped = para.strip()
            if stripped and stripped not in seen:
                deduped.append(stripped)
                seen.add(stripped)
        return "\n\n".join(deduped)
    
    def deduplicate_list(items):
        if not isinstance(items, list):
            return []
        seen = set()
        cleaned = []
        for item in items:
            stripped = item.strip()
            if stripped and stripped not in seen:
                cleaned.append(stripped)
                seen.add(stripped)
        return cleaned
    
    executive_summary = deduplicate_paragraphs(executive_summary)
    client_email = deduplicate_paragraphs(client_email)
    action_items = deduplicate_list(action_items)

    deliverables = {
        "executive_summary": executive_summary,
        "client_email": client_email,
        "action_items": action_items,
        "citations": citations
    }

    # final_answer = f"""
    #     EXECUTIVE SUMMARY
    #     {executive_summary}

    #     CLIENT EMAIL
    #     {client_email}

    #     ACTION ITEMS
    #     {action_items}
    #     {citations}
    # """

    return {
        "deliverables": deliverables,
        # "final_answer": final_answer,
        "trace": state.trace + [{
            "step": "Write",
            "agent": "Writer",
            "action": "Generated multi-output deliverable",
            "outcome": "Success"
        }]
    }

