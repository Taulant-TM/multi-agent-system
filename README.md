# Agentic Research & Action Assistant  
*A LangGraph-based Multi-Agent RAG System*

---

## Overview

The **Agentic Research & Action Assistant** is a multi-agent Retrieval-Augmented Generation (RAG) system built with **LangGraph**.

It orchestrates a structured workflow using specialized agents:

- **Planner** – Creates an execution plan  
- **Researcher** – Retrieves relevant documents  
- **Writer** – Generates structured, citation-backed outputs  
- **Reviewer** – Verifies grounding, coverage, and safety  

The system produces business-ready deliverables such as executive summaries, client emails, action lists, and internal documentation.

---

## Core Features

- LangGraph multi-agent orchestration  
- Retrieval-augmented generation (RAG)  
- Inline citation enforcement  
- Prompt injection defense  
- Verifier-driven rewrite loop (max 3 iterations)  
- Confidence scoring  
- Multi-output generation mode  
- Automated evaluation suite  
- Streamlit UI with trace timeline  

---

## Supported Tasks

The assistant supports:

- Risk analysis and mitigation proposals  
- Client update emails  
- Comparative approach recommendations  
- Deadline and owner extraction  
- Internal documentation drafting  
- Architecture dependency analysis  
- Executive project summaries  

All task types are validated through automated evaluation tests.

---

## Safety & Verification

The Reviewer enforces:

- Grounded responses only  
- Citation presence  
- Coverage completeness  
- Confidence scoring (0–1)  
- Automatic rejection of ungrounded outputs  

Research documents are treated strictly as **data**, not instructions.

---

## Evaluation

Located in `/eval`.

Run:

```bash
python -m eval.run_eval
```

## Installation
```bash
git clone <repo-url>
cd agentic-research-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
## Run the app:
```bash
streamlit run streamlit_app.py
```
