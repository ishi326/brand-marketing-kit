"""
uses LangGraph to create a flowchart that describes the flow of the model
"""
from langgraph.graph import StateGraph, END

from src.state import PipelineState
from src.agents import (
    research_node,
    strategy_node,
    critique_node,
    creative_node,
    route_after_critique,
)

def build_graph():
    graph = StateGraph(PipelineState)
    graph.add_node("research", research_node)
    graph.add_node("strategy", strategy_node)
    graph.add_node("critique", critique_node)
    graph.add_node("creative", creative_node)
    graph.set_entry_point("research")
    graph.add_edge("research", "strategy")
    graph.add_edge("strategy", "critique")
    graph.add_conditional_edges(
        "critique",
        route_after_critique,
        {
            "revise": "strategy",
            "approve": "creative",
        },
    )
    graph.add_edge("creative", END)
    return graph.compile()