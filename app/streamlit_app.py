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

    st.subheader("Final Answer")
    final_answer = result.get("final_answer")
    review_status = result.get("review_status")

    deliverables = result.get("deliverables", {})

    if deliverables:
        st.subheader("Executive Summary")
        st.write(deliverables.get("executive_summary"))

        st.subheader("Client Email")
        st.write(deliverables.get("client_email"))

        st.subheader("Action Items")
        st.write(deliverables.get("action_items"))

        st.subheader("Sources")
        st.write(deliverables.get("citations"))

    if not final_answer:
        st.warning("No final answer produced.")
    elif review_status == "rejected":
        st.warning("⚠️ Answer was generated but rejected by the Reviewer.")
        st.write(final_answer)
    else:
        if not deliverables:
            st.write(final_answer)

    st.subheader("Review")
    st.write(result.get("review", "No review produced."))
    st.write("Status:", result.get("review_status"))

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

