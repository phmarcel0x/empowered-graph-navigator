# 5COM2003: Artificial Intelligence
# Practical Assignment: Variant A - Graph Measures
# Marcelo Hernandez: 23033126
# main.py

import graph as g
import agent as a
import random
import csv

# Create an instance of the Graph class
g1 = g.Graph()  
g1.create_graph()
a1 = a.Agent(g1)

print("\nBFS SHORTEST PATH RESULTS:")
for node in g1.nodes:
    g1.display_bfs(g1.nodes[node])

metrics_g1 = g.GraphMetrics(g1)
metrics_g1.save_metrics("graph_metrics.csv")
metrics_g1.display()

# Run simulations
simulations = 1000
results = []

for _ in range(simulations):
    nodes_list = list(g1.get_nodes().values())  # Convert node objects to a list
    start = random.choice(nodes_list)
    target = random.choice(nodes_list)
    while target == start: 
        target = random.choice(nodes_list)  # Choose a new target if it is the same as the start node

    # Random Walk simulation
    a1.memory = []  # Reset memory (probably better if I did this in the Agent class)
    a1.random_walk(start, target) 
    random_walk_nodes_visited = len(a1.memory)  # Store the number of nodes visited during the random walk

    # Shortest Path simulation
    a1.memory = []
    a1.shortest_path(start, target)
    shortest_path_nodes_visited = len(a1.memory)  # Store the number of nodes visited during the shortest path search

    results.append([start.get_name(), target.get_name(), random_walk_nodes_visited, shortest_path_nodes_visited])

# Save results to a CSV file for analysis
filename = "sim_results.csv"
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Start Node", "Target Node", "Random Walk # of Visited Nodes", "Shortest Path # of Visited Nodes"])
    writer.writerows(results)
     
print("\nSimulations completed and results saved to:", filename)