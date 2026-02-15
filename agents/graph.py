from langgraph.graph import StateGraph, END
from agents.state import WorkflowState

from agents.planner import planner_agent
from agents.researcher import research_agent
from agents.answerer import answer_agent
from agents.reviewer import reviewer_agent


def build_graph():
    graph = StateGraph(WorkflowState)

    graph.add_node("Planner", planner_agent)
    graph.add_node("Researcher", research_agent)
    graph.add_node("Writer", answer_agent)
    graph.add_node("Reviewer", reviewer_agent)

    graph.set_entry_point("Planner")

    def planner_router(state):
        if state.needs_research:
            return "Researcher"
        return "Writer"

    graph.add_conditional_edges("Planner", planner_router)
    graph.add_edge("Researcher", "Writer")

    def review_router(state):
        if state.review_status == "approved":
            return END
        return "Writer"

    graph.add_edge("Writer", "Reviewer")
    graph.add_conditional_edges("Reviewer", review_router)

    return graph.compile()