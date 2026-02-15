from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from agents.state import WorkflowState


load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini",temperature = 0)

def planner_agent(state: WorkflowState):

    task = state.task

    prompt = f"""
    You are a planning agent.

    Task:
    {task}

    Decide required steps from:
    - Research
    - Write
    - Review

    Steps:
    - Research: yes/no
    - Write: yes
    - Review: yes
    """
    

    plan_text = llm.invoke(prompt).content

    needs_research = "research: no" not in plan_text.lower()

    return {
        "plan": plan_text,
        "needs_research": needs_research,
        "trace": state.trace + [{
            "step": "Plan",
            "agent": "Planner",
            "action": "Generated plan",
            "outcome": "Success",
            "needs_research": needs_research
        }]
    }
