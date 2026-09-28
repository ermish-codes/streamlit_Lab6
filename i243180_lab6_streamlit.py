import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Hospital Search Agent",
    layout="wide"
)

st.title("Hospital Emergency Supply Robot - Search Visualizer")
st.write("Select an initial node, a goal node, and a search algorithm to visualize the solution path.")

# ============================================================
# NODE SELECTION
# ============================================================
nodes = list(hospital_graph.keys())

start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)

# ============================================================
# RUN SEARCH
# ============================================================
if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost, expansion_order = gbfs(start, goal, hospital_graph)
    else:
        path, cost, expansion_order = a_star(start, goal, hospital_graph)

    if path is None or len(path) == 0:
        st.error("No path found between the selected nodes.")
    else:
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' -> '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Expansion Order:** {' -> '.join(expansion_order)}")

        # ============================================================
        # VISUALIZE NETWORKX GRAPH
        # ============================================================
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(figsize=(10, 6))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2000, ax=ax)

        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, ax=ax)

        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

        # Draw edge weights
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

        # Highlight solution path
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2, arrows=True, ax=ax)

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")

        st.pyplot(fig)