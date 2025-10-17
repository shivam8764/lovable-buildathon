from typing import Dict, Any
import networkx as nx
from app.services.concept_service import get_subgraph
from app.services.progress_service import get_user_progress

def build_graph(subgraph: Dict[str, Any]) -> nx.DiGraph:
    G = nx.DiGraph()
    for n in subgraph["nodes"]:
        G.add_node(n["name"], **n)
    for e in subgraph["edges"]:
        G.add_edge(e["source"], e["target"], weight=e.get("weight", 0.7))
    return G

async def adaptive_map(user_id: str, topic: str, depth: int = 2) -> Dict[str, Any]:
    sg = await get_subgraph(topic, depth)
    G = build_graph(sg)
    user = await get_user_progress(user_id)
    mastery = user.get("summary_vector", {})

    # decorate nodes with mastery and rank
    nodes = []
    for n in G.nodes:
        m = float(mastery.get(n, 0.0))
        rank = 1.0 - m  # lower mastery -> higher priority
        nodes.append({"name": n, "mastery": m, "priority": rank})

    edges = [{"source": u, "target": v, "weight": float(G[u][v].get("weight", 0.7))} for u, v in G.edges]

    # naive next suggestions: nodes with lowest mastery among immediate neighbors
    immediate = set(G.successors(topic)) | set(G.predecessors(topic))
    suggestions = sorted(
        [{"topic": n, "mastery": float(mastery.get(n, 0.0))} for n in immediate],
        key=lambda x: x["mastery"]
    )[:5]

    return {
        "center": topic,
        "nodes": nodes,
        "edges": edges,
        "suggested_next": suggestions
    }
