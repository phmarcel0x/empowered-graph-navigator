# Marcelo Hernandez - May 2024
# agent.py

import graph
import random

# Agent Class
class Agent:
    def __init__(self, graph):
        self.graph = graph
        self.memory = []  # List to store visited nodes during simulations

    def random_walk(self, start, target):
        current_node = start  
        self.memory.append(current_node)  # Store the current node in memory
        while current_node != target:  # Continue until the targt node is reached
            neighbours = current_node.get_neighbours() 
            next_node = random.choice(neighbours)
            current_node = next_node  # Move to the next node
            self.memory.append(current_node)  # Store the new current node in memory
        return current_node

    def shortest_path(self, start, target):
        path = self.graph.bfs_shortest_path_mod(start, target)  # Use the modified BFS method
        if path:
            self.memory.extend(path[0])  # Store all nodes in the shortest path in memory
        return path