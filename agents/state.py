from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class WorkflowState(BaseModel):
    task: str
    plan: Optional[str] = None
    research_notes: List[Dict[str, Any]] = Field(default_factory=list)
    final_answer: Optional[str] = None
    review_status: Optional[str] = None
    review: Optional[str] = None
    trace: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: Optional[float] = None
    needs_research: Optional[bool] = True
    iteration_count: int = 0
    deliverables: dict = {}




