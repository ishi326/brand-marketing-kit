"""
Defines the shared data structure (PipelineState) that gets passed between every agent
"""

from typing import Optional, TypedDict
from src.schemas import ContentIdeaList, CritiqueResult

class PipelineState(TypedDict, total=False):
    # Inputs
    brand_url: str
    max_revisions: int
    demo_mode: bool

    # Raw ingested data
    brand_site_data: dict
    competitor_results: list[dict]

    # Research Agent
    research_brief: str

    # Strategy Agent
    strategy: str
    strategy_rationale: str

    # Critique Agent
    critique: CritiqueResult
    revision_count: int
    critique_history: list[str]

    # Creative Agent
    content_ideas: ContentIdeaList