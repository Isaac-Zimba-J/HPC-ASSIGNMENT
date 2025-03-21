
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

# ----------------- CONFIGURATION -----------------
D = 4  # Dimension of the hypercube (Adjust this for more nodes)
MESSAGE_LIFETIME = 5  # How many hops a message can survive
INTERVAL = 1000  # Milliseconds between frames

# ----------------- HYPERCUBE CREATION -----------------
G = nx.hypercube_graph(D)
pos = nx.spring_layout(G, seed=42)  # Positioning nodes for visualization
active_messages = []  # List of active messages (sender, receiver, hops)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title(f"{D}-Dimensional Hypercube HPC Simulation")

# ----------------- ANIMATION FUNCTION -----------------
def update(frame):
    ax.clear()
    ax.set_title(f"{D}-Dimensional Hypercube HPC Simulation | Frame {frame}")

    # Draw static network
    nx.draw(G, pos, with_labels=True, node_color="lightgray", edge_color="gray", node_size=800, font_size=10)

    # Add new messages randomly
    if random.random() < 0.5:  # Probability of new message
        sender = random.choice(list(G.nodes))
        neighbors = list(G.neighbors(sender))
        if neighbors:
            receiver = random.choice(neighbors)
            active_messages.append([sender, receiver, MESSAGE_LIFETIME])  # Message starts with full life

    # Process active messages
    new_messages = []
    for msg in active_messages:
        sender, receiver, lifetime = msg
        if lifetime > 0:
            nx.draw_networkx_nodes(G, pos, nodelist=[sender], node_color="red", node_size=800)  # Sender in red
            nx.draw_networkx_nodes(G, pos, nodelist=[receiver], node_color="green", node_size=800)  # Receiver in green
            nx.draw_networkx_edges(G, pos, edgelist=[(sender, receiver)], edge_color="blue", width=2)  # Message path
            lifetime -= 1  # Decrease message lifetime
            if lifetime > 0:  # Continue propagating
                new_neighbors = list(G.neighbors(receiver))
                if new_neighbors:
                    new_receiver = random.choice(new_neighbors)
                    new_messages.append([receiver, new_receiver, lifetime])

    active_messages[:] = new_messages  # Update active messages

# ----------------- RUNNING ANIMATION -----------------
ani = animation.FuncAnimation(fig, update, frames=50, interval=INTERVAL, repeat=True)
plt.show()



