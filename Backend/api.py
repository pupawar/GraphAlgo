from flask import Blueprint, request, jsonify
from collections import defaultdict
from models import db, nodes, edges
import heapq
api = Blueprint('api', __name__)

@api.route('/create_undirected_graph', methods=['POST'])
def create_undirected_grap():
    data = request.get_json()
    nodes_list = data.get('nodes', [])
    edges_list = data.get('edges', [])
    
    for  elem in nodes_list:
        new_node = nodes(id=elem['id'], name=elem['name'])
        db.session.add(new_node)

    db.session.commit()
    
    for elem in edges_list:
        new_edge = edges(id=elem['id'], source=elem['source'], target=elem['target'], weight=elem['weight'])
        db.session.add(new_edge)
    
    
    db.session.commit()
    return "SUCCESSFUL"

@api.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()

    node_id = data.get('id')
    node_name = data.get('name')

    new_node = nodes(id=node_id, name=node_name)
    db.session.add(new_node)
    db.session.commit()

    return "SUCCESSFUL"
    
@api.route('/delete_node', methods=['POST'])
def delete_node():
    data = request.get_json()
    node_id = data.get('id')

    edges.query.filter((edges.source == node_id) | (edges.target == node_id)).delete()
    
    nodes.query.filter_by(id=node_id).delete()
    
    db.session.commit()
    return "SUCCESSFUL"

@api.route('/add_edge', methods=['POST'])
def add_edge():
    data = request.get_json()
    edge_id = data.get('id')
    source = data.get('source')
    target = data.get('target')
    weight = data.get('weight')     

    new_edge = edges(id=edge_id, source=source, target=target, weight=weight)
    db.session.add(new_edge)
    db.session.commit()
    return "SUCCESSFUL"

@api.route('/delete_edge', methods=['POST'])
def delete_edge():
    data = request.get_json()
    edge_id = data.get('id')

    edges.query.filter_by(id=edge_id).delete()
    db.session.commit()
    return "SUCCESSFUL"

@api.route('/edit_edge', methods=['POST'])
def edit_edge():
    data = request.get_json()
    edge_id = data.get('id')
    weight = data.get('weight')

    edge = edges.query.filter_by(id=edge_id).first()
    if edge:
        edge.weight = weight
        db.session.commit()
        return "SUCCESSFUL"
    return "Edge not found", 404

@api.route('/get-graph', methods=['GET'])
def get_graph():
    all_edges = edges.query.all()
    all_nodes = nodes.query.all()
    nodes_list = {}
    edges_list = {}
    for elem in all_edges:
        edges_list[elem.id] = {"source" : elem.source, "target" : elem.target, "label": elem.weight}
    for node in all_nodes:
        nodes_list[node.id] = {"name" : node.name}

    graph = {"nodes" : nodes_list, "edges" : edges_list}
    return jsonify(graph)
    ##return jsonify(graph)

def create_adjacency_list(adj_list):
    all_edges = edges.query.all()
    for elem in all_edges:
        adj_list[elem.source].append([elem.target, elem.weight])
        adj_list[elem.target].append([elem.source, elem.weight])

def create_node_dist(node_dist, node_neighbor, source):
    node_dist[source] = 0
    all_nodes = nodes.query.all()
    for node in all_nodes:
        if node.id != source:
            node_dist[node.id] = float('inf')  
            node_neighbor[node.id] = -1

@api.route('/get_undirected_shortest_path', methods=['POST'])
def get_undirected_shortest_path():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415
            
        data = request.get_json()
        source = data.get('source')
        target = data.get('target')

    except Exception as e:
        print(f"Error getting source/target: {e}")
        return jsonify({"error": "Failed to get source and target"}), 400
    
    adjacency_list = defaultdict(list)
    create_adjacency_list(adjacency_list)

    node_dist = defaultdict(int)
    node_neighbor = defaultdict(int);
    create_node_dist(node_dist, node_neighbor, source)
    visited = set()
    #Dijkstra's algorithm
    min_heap = [[0,source]]
    while min_heap:
        currentdist, current_node = heapq.heappop(min_heap)
        visited.add(current_node)
        print('-------------')
        print(node_dist)
        for neighbors in adjacency_list[current_node]:
            print('hi')
            print(neighbors)
            neighbor, weight = neighbors
            if node_dist[neighbor] > node_dist[current_node] + weight and neighbor not in visited:
                node_dist[neighbor] = node_dist[current_node] + weight
                node_neighbor[neighbor] = current_node
                heapq.heappush(min_heap, (node_dist[neighbor], neighbor))

    # path = []
    # current_node = target
    # while current_node != -1 and current_node != source:
    #     path.append(current_node)
    #     current_node = node_neighbor[current_node]
    # path.reverse()

    # print(path)
    # return jsonify({"path" : path, "distance" : node_dist[target]})
    return "DONE"
