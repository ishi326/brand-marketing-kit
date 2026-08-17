"""
Creates the three different pydantic tables that guide Ai responses by the agents in a particular format
"""
from pydantic import BaseModel, Field
from typing import Literal 

class CritiqueResult (BaseModel):
    decision: Literal["APPROVE", "REVISE"] = Field(description = "APPROVE only if all five checks(boolean fields) are true")
    brand_alignment: bool = Field(description= "TRUE only if the strategy aligns with the brand, its positioning and aesthetic")
    evidence_support: bool = Field(description = "TRUE only if the strategy is derived from evidence found furing the research phase previously")
    commercial_viability: bool = Field(description = "TRUE only if it is viable to commericially execute the strategy")
    differentiability: bool = Field(description= "TRUE only if the strategy isn't the exact copy/replica of a competitior")
    feasibility: bool = Field(description = "TRUE only if the strategy is realistic, feasible and does not raise significant risks")
    feedback: str = Field(description="constructive, concise feedback that can help the next strategy meet more of the checks")

class ContentIdea(BaseModel):
    idea: str = Field(description="Short title for the content piece that is direct and easy to understand")
    format: str = Field(description="Content format which is how should the idea be presented to the user. Eg: reel, carousel, whatsapp etc.")
    highlight: str = Field(description="The opening hook or standout moment that should be how to target the user")
    concept: str = Field(description="2-3 sentence description of the idea and how it will roll out")
    cta: str = Field(description="The call to action for this piece")
    purpose: str = Field(description="2-3 sentences on why this strategy should exist and how it will benefit the company")

class ContentIdeaList(BaseModel):
    ideas: list[ContentIdea] = Field(description="5 to 6 distinct ideas covering a mix of formats")
