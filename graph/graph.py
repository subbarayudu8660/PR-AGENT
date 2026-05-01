from langgraph.graph import StateGraph, START, END
from state.state import ReviewState
from nodes.security import security_node
from nodes.performance import performance_node
from nodes.style import style_node
from nodes.aggregator import aggregator_node
from nodes.ranker import ranker_node

def build_graph():
    builder = StateGraph(ReviewState)

    builder.add_node("security", security_node)
    builder.add_node("performance", performance_node)
    builder.add_node("style", style_node)
    builder.add_node("aggregator", aggregator_node)
    builder.add_node("ranker", ranker_node)

    builder.add_edge(START, "security")
    builder.add_edge(START, "performance")
    builder.add_edge(START, "style")
    builder.add_edge("security", "aggregator")
    builder.add_edge("performance", "aggregator")
    builder.add_edge("style", "aggregator")
    builder.add_edge("aggregator", "ranker")
    builder.add_edge("ranker", END)

    return builder.compile()