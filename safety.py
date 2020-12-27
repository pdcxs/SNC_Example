# -*- coding utf-8 -*-
# graph is an edge list
# an edge is (start_id, end_id)
# degree is 
def calculate_degrees(graph):
    degrees = {}
    def add_degree(node, degree):
        if node in degree:
            degree[node] += 1
        else:
            degree[node] = 1
    
    for (start, end) in graph:
        add_degree(start, degrees)
        add_degree(end, degrees)
    
    return degrees

def get_degree(id, degrees):
    if id in degrees:
        return degrees[id]
    else:
        return 0
    
# safety calculation
# sum up multiply degrees of ends of each edge
def calculate_safety(graph):
    degrees = calculate_degrees(graph)
    s = 0
    for (start, end) in graph:
        s += get_degree(start, degrees) * get_degree(end, degrees)
    node_num = len(degrees)
    max_s = node_num * ((node_num - 1) ** 3) / 2
    return s / max_s

if __name__ == "__main__":
    graph1 = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
    graph2 = [(1, 2), (2, 3), (1, 3), (1, 5), (3, 5), (3, 4), (4, 5)]
    
    degrees1 = calculate_degrees(graph1)
    degrees2 = calculate_degrees(graph2)
    
    safety1 = calculate_safety(graph1)
    safety2 = calculate_safety(graph2)
    
    print("degrees of graph: ")
    print(graph1)
    print(degrees1)
    
    print("degrees of graph: ")
    print(graph2)
    print(degrees2)
    
    print("safety values:")
    print(safety1, safety2)
    