"""
File that contains all 4 AI agent models. Each model contains a system prompt and a user prompt. 
Followed by feeding the prompt into the LLM and recording responses.
"""

from langchain_core.prompts import ChatPromptTemplate
from src.config import get_llm
from src.schemas import ContentIdeaList, CritiqueResult

def extract_text(content) -> str:
    """Gemini returns content as a list of blocks instead of a plain string. Converts to String"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        ]
        return "\n".join(parts)
    return str(content)

# 1. Research Agent

research_prompt = """You are a marketing researcher preparing a research brief for a company. 
Work only from the material provided and do not invent any facts. Imagine you are briefing the marketing team. 
Structure your brief into the following sections and make sure you adhere to them. 1. Brand Overview (what brand sells, category of product)
2. Brand positioning (aesthetic, goal, reach, market niche) 3. Products/Services 4. Target Audience and Target cities/locations
5. Competitors, only if there are, otherwise no 6. Market opportunities, a few (2-4) growth oportunities. 
The more specific you are pertaining to the brand without hallucinating, the better.
Write in plain text. Do not use markdown formatting (no asterisks, no headers, no bullet symbols).
Keep each section to 2-3 concise sentences. Total brief should be under 250 words."""

research_user_prompt = """ brand website data - URL: {brand_url} Title: {brand_title} Meta description: {brand_meta} Page text: {brand_text}{brand_error}
Competitor search results: {competitor_section}
Write the research brief now."""

def research_node(state: dict) -> dict:
    brand = state.get("brand_site_data") or {}
    competitors = state.get("competitor_results") or []
    if competitors:
        competitor_section = "\n".join(
            f"- {c.get('title')}: {c.get('body')} ({c.get('href')})" for c in competitors
        )
    else:
        competitor_section = "Not available: infer likely competitors from the brand's category."

    prompt = ChatPromptTemplate.from_messages(
        [("system", research_prompt), ("user", research_user_prompt)]
    )
    chain = prompt | get_llm()
    result = chain.invoke({
        "brand_url": state.get("brand_url"),
        "brand_title": brand.get("title") or "(unknown)",
        "brand_meta": brand.get("meta_description") or "(none found)",
        "brand_text": (brand.get("text") or "(no text retrieved)")[:5000],
        "brand_error": f"(Note: {brand['error']})" if brand.get("error") else "",
        "competitor_section": competitor_section,
    })
    return {"research_brief": extract_text(result.content)}

# 2. Strategy Agent

strategy_prompt = """You are a  marketing strategist for small companies with limited budgets and small teams. 
Given a research brief, give suggestions to solve one major question: "How should this brand grow sales through online marketing?"
Produce a single, coherent, clear strategy and a reasoning/rationale as to why this strategy is THE best strategy for the company. 
This strategy must be grounded in evidence from the research brief and try to keep it realistic.
Write in plain text. Do not use markdown formatting (no asterisks, no headers, no bullet symbols).
Keep the strategy to 2-3 sentences and the rationale to 3-4 sentences.no more."""

strategy_user_prompt = """ research brief {research_brief}{revision_context} Write the strategy and reasoning now. Format your response as:
Strategy: <the strategy>
Reasoning: <the reasoning>"""

def strategy_node(state: dict) -> dict:
    revision_context = ""
    history = state.get("critique_history") or []
    if history:
        revision_context = (
            "Previous strategy was sent back from the critique model. Address this feedback:\n"
            + "\n".join(f"- {fb}" for fb in history)
        )

    prompt = ChatPromptTemplate.from_messages(
        [("system", strategy_prompt), ("user", strategy_user_prompt)]
    )
    chain = prompt | get_llm()

    result = chain.invoke({
        "research_brief": state.get("research_brief", ""),
        "revision_context": revision_context,
    })
    strategy, rationale = _split_strategy_rationale(extract_text(result.content))
    return {"strategy": strategy, "strategy_rationale": rationale}

def _split_strategy_rationale(text: str) -> tuple[str, str]:
    strategy, rationale = text, ""
    upper = text.upper()
    if "REASONING:" in upper:
        idx = upper.index("REASONING:")
        strategy = text[:idx].replace("STRATEGY:", "").strip()
        rationale = text[idx + len("REASONING:"):].strip()
    return strategy, rationale


# 3. Critique Agent

critique_prompt = """You are a critic reviewing a strategy before it gets built into content. Actively look for reasons this strategy could fail.
Evaluate against the following criteria: 
- Brand alignment: does it fit the brand's identity and voice?
- Evidence support: is it grounded in the research brief, not generic advice?
- Commercial viability: is there a credible path to more sales?
- Differentiability: does it meaningfully differ from competitors?
- Feasibility: can a small company realistically execute this without major risk?

Only APPROVE if it clearly passes all five. Otherwise REVISE with specific,
actionable feedback. Something the Strategy agent can work on.
Write in plain text. Do not use markdown formatting (no asterisks, no headers, no bullet symbols).
"""

critique_user_prompt = """research brief {research_brief} proposed strategy {strategy} reasoning {reasoning}. Evaluate this strategy now."""

def critique_node(state: dict) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [("system", critique_prompt), ("user", critique_user_prompt)]
    )
    llm = get_llm().with_structured_output(CritiqueResult)
    chain = prompt | llm
    critique: CritiqueResult = chain.invoke({
        "research_brief": state.get("research_brief", ""),
        "strategy": state.get("strategy", ""),
        "reasoning": state.get("strategy_reasoning", ""),
    })
    revision_count = state.get("revision_count", 0)
    history = list(state.get("critique_history") or [])

    if critique.decision == "REVISE":
        revision_count += 1
        history.append(critique.feedback)

    return {
        "critique": critique,
        "revision_count": revision_count,
        "critique_history": history,
    }

def route_after_critique(state: dict) -> str:
    """Conditional edge: revise loops back to strategy (up to max_revisions), else creative."""
    critique = state.get("critique")
    max_revisions = state.get("max_revisions", 3)
    revision_count = state.get("revision_count", 0)

    if critique is not None and critique.decision == "REVISE" and revision_count < max_revisions:
        return "revise"
    return "approve"

# 4. Creative Agent

creative_prompt = """You are a social media first creative director. Given an approved marketing strategy, generate 5-6 concrete 
content ideas that execute it. Mix formats (Reels, carousels, UGC prompts, etc). Each idea must be specific to this brand. Avoid generic filler.
Write in plain text. Do not use markdown formatting (no asterisks, no headers, no bullet symbols).Keep feedback to 2-3 sentences"""

creative_user_prompt = """research brief {research_brief} approved strategy {strategy} reasoning {reasoning} Generate 5 to 6 content ideas now."""

def creative_node(state: dict) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [("system", creative_prompt), ("user", creative_user_prompt)]
    )
    llm = get_llm().with_structured_output(ContentIdeaList)
    chain = prompt | llm

    ideas: ContentIdeaList = chain.invoke({
        "research_brief": state.get("research_brief", ""),
        "strategy": state.get("strategy", ""),
        "reasoning": state.get("strategy_reasoning", ""),
    })
    return {"content_ideas": ideas}