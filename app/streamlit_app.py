import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from agents.orchestrator import run_workflow
import pandas as pd

st.title("Agentic Research & Action Assistant")

task = st.text_input("Enter your task")
run = st.button("Run")

if run and task:
    with st.spinner("Running multi-agent workflow..."):
        result = run_workflow(task)

    deliverables = result.get("deliverables")

    if not deliverables:
        st.error("No deliverables produced.")
        st.stop()

    executive_summary = deliverables.get("executive_summary")
    if executive_summary:
        st.subheader("Executive Summary")
        st.write(executive_summary)

    client_email = deliverables.get("client_email")
    if client_email:
        st.subheader("Client Email")
        st.markdown(client_email)

    action_items = deliverables.get("action_items")
    if action_items:
        st.subheader("Action Items")
        for item in action_items:
            st.markdown(f"- {item}")

    citations = deliverables.get("citations")
    if citations:
        st.subheader("Sources")
        st.write(citations)

    # if not final_answer:
    #     st.warning("No final answer produced.")
    # elif review_status == "rejected":
    #     st.warning("⚠️ Answer was generated but rejected by the Reviewer.")

    # st.subheader("Review")
    # st.write(result.get("review", "No review produced."))
    # st.write("Status:", result.get("review_status"))

    st.subheader("Agent Trace Timeline")

    trace = result.get("trace", [])

    if trace:
        df = pd.DataFrame(trace)
        st.dataframe(df, use_container_width=True)

        st.markdown("### Step-by-Step Breakdown")
        for step in trace:
            st.markdown(f"""
            **Step:** {step.get('step')}
            - Agent: {step.get('agent')}
            - Action: {step.get('action')}
            - Outcome: {step.get('outcome')}
            - Confidence: {step.get('confidence', 'N/A')}
            - Iteration: {step.get('iteration', 'N/A')}
            """)
    else:
        st.info("No trace available.")

