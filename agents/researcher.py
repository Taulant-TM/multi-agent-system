from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from agents.state import WorkflowState
import re

load_dotenv()

vectorstore = FAISS.load_local(
    "data/index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

def sanitize_content(text: str) -> str:
    if not text:
        return text

    injection_regex = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s+prompt",
        r"you\s+are\s+chatgpt",
        r"act\s+as\s+",
        r"override\s+instructions",
        r"disregard\s+rules",
        r"developer\s+message",
        r"assistant\s+must",
        r"do\s+anything\s+now",
        r"jailbreak"
    ]

    lowered = text.lower()

    for pattern in injection_regex:
        if re.search(pattern, lowered):
            return "[REMOVED: potential prompt injection content]"

    return text

def research_agent(state: WorkflowState):

    plan = state.plan or ""
    docs = vectorstore.similarity_search(plan, k=4)

    notes = []
    for doc in docs:
        clean_content = sanitize_content(doc.page_content)
        notes.append({
            "content": clean_content,
            "source": doc.metadata.get("source")
    })

    return {
        "research_notes": notes,
        "trace": state.trace + [{
            "step": "Research",
            "agent": "Researcher",
            "action": "Vector search",
            "outcome": f"{len(notes)} notes retrieved"
        }]
    }
