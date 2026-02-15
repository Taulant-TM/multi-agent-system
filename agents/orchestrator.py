from agents.graph import build_graph

def run_workflow(task: str):
    graph = build_graph()

    initial_state = {
        "task": task,
        "trace": [],
        "research_notes": [],  
        "final_answer": None
    }

    final_state = graph.invoke(initial_state)
    return final_state
