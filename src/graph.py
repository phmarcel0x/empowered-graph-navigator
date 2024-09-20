# 5COM2003: Artificial Intelligence
# Practical Assignment: Variant A - Graph Measures
# Marcelo Hernandez: 23033126
# graph.py

from collections import deque
import csv

# Node Class
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        
    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
    
    def get_neighbours(self):
        return self.neighbours
    
    def get_name(self):
        return self.name

    def get_degree(self):
        return len(self.neighbours)


# Edge Class
class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
    
    def get_nodes(self):
        return self.node1, self.node2


# Undirected Graph Class
class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes
        self.edges = []  # List to store edges 
        self.node_count = 0 
        self.edge_count = 0 
        
    def add_node(self, node):
        self.nodes[node.get_name()] = node  
        self.node_count += 1
        
    def add_edge(self, edge):
        node1, node2 = edge.get_nodes()
        self.nodes[node1.get_name()].add_neighbour(node2)
        self.nodes[node2.get_name()].add_neighbour(node1)
        self.edges.append(edge)  # Store the edge
        self.edge_count += 1
        
    def get_nodes(self):
        return self.nodes
    
    def get_edges(self):
        return self.edges

    def bfs_shortest_path(self, start):
        distances = {}  
        queue = deque([start])  # Begin with the start node
        distances[start.get_name()] = 0  # Distance to itself is 0

        while queue:
            node = queue.popleft()  # Remove the first node from the queue (FIFO)
            current_distance = distances[node.get_name()]  
            for neighbour in node.get_neighbours():
                # Check if not visited (through the distances dictionary)
                if neighbour.get_name() not in distances:  
                    queue.append(neighbour)  # Add the neighbour to the queue to be visited
                    distances[neighbour.get_name()] = current_distance + 1  # Increment the distance by 1              
        return distances
    
    def bfs_shortest_path_mod(self, start, target):
        queue = deque([(start, [start.get_name()])])  # get_name() included because the path is a list of names
        visited = set()  
        shortest_paths = []
        shortest_length = float('inf')  # Infinity used to compare the shortest path

        while queue:
            current_node, path = queue.popleft()  # Remove the first node from the queue (FIFO)
            # Check if not visited or shorter path (through the visited set and shortest_length variable)
            if current_node not in visited or len(path) <= shortest_length:  
                visited.add(current_node)  
                # Add the path to the shortest_paths if the target is reached
                if current_node == target:
                    shortest_length = len(path)
                    shortest_paths.append(path)
                # Extend the path to the neighbors not yet visited
                for neighbor in current_node.get_neighbours():
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor.get_name()]))

        # Return only the shortest paths from the collected paths in the queue
        return [p for p in shortest_paths if len(p) == shortest_length]
    
    def display_bfs(self, start):
        distances = self.bfs_shortest_path(start)  
        print(f"{start.get_name()} to: {distances} => SUM = {sum(distances.values())}")
    
    def display(self):
        for node in self.nodes:
            # List comprehension is a wonderful thing
            print(f"{node} neighbours: {[neighbour.get_name() for neighbour in self.nodes[node].get_neighbours()]}")

    # Create the graph
    def create_graph(self):
        print("\nGRAPH DISPLAY:")
        
        for i in range(1, 8):
            self.add_node(Node('V' + str(i)))
        
        self.add_edge(Edge(self.nodes['V1'], self.nodes['V2']))
        self.add_edge(Edge(self.nodes['V2'], self.nodes['V3']))
        self.add_edge(Edge(self.nodes['V3'], self.nodes['V4']))
        self.add_edge(Edge(self.nodes['V4'], self.nodes['V5']))
        self.add_edge(Edge(self.nodes['V3'], self.nodes['V6']))
        self.add_edge(Edge(self.nodes['V6'], self.nodes['V7']))
        self.add_edge(Edge(self.nodes['V7'], self.nodes['V4']))

        self.display()
    
            
# Graph Metrics Class
# As defined in Clements (2019)
class GraphMetrics:
    def __init__(self, graph):        
        self.graph = graph
        
    def degree_centrality(self, node):
        return node.get_degree()  
    
    def closeness_centrality(self, node):
        distances = self.graph.bfs_shortest_path(node)
        total_distance = sum(distances.values())  
        closeness_cent = 0
        if total_distance > 0:  # Avoid division by zero
            closeness_cent = 1 / total_distance
        return closeness_cent
    
    def betweenness_centrality(self, node):
        betweenness = 0
        nodes = self.graph.get_nodes().values()
        for start in nodes:
            for target in nodes:
                # Check if start and target are different from the node
                if start != target and start != node and target != node:
                    # Get all shortest paths between start and target
                    all_paths = self.graph.bfs_shortest_path_mod(start, target)  
                    # Fitler the paths that contain the node
                    shortest_paths_through_node = [path for path in all_paths if node.get_name() in path]  
                    # Increment the betweenness if the node is in the path unless all_paths is empty
                    betweenness += len(shortest_paths_through_node) / len(all_paths) if all_paths else 0
        return betweenness
    
    # Display the metrics for all nodes
    def display(self):
        print("\nGRAPH METRICS:")
        for node in self.graph.get_nodes().values():
            # self.degree_centrality(node)
            print(f"- {node.get_name()} Degree Centrality = {self.degree_centrality(node)}")
            print(f"- {node.get_name()} Closeness Centrality = {self.closeness_centrality(node)}")
            print(f"- {node.get_name()} Betweenness Centrality = {self.betweenness_centrality(node)}")
            print()
        
    # Save the metrics to a CSV file
    def save_metrics(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Node", "Degree Centrality", "Closeness Centrality", "Betweenness Centrality"])
            for node in self.graph.get_nodes().values():
                writer.writerow([node.get_name(), node.get_degree(), self.closeness_centrality(node), self.betweenness_centrality(node)])