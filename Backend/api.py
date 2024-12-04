
from flask import Blueprint, request, jsonify
from collections import defaultdict
from models import db, nodes, edges
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
        new_edge = edges(source=elem['source'], target=elem['target'], weight=elem['weight'])
        db.session.add(new_edge)

    db.session.commit()
    return "SUCCESSFUL"

@api.route('/get-graph', methods=['GET'])
def get_graph():
    all_edges = edges.query.all()
    all_nodes = nodes.query.all()
    nodes_list = {}
    edges_list = {}
    counter =0
    for elem in all_edges:
        edges_list[counter] = {"source" : elem.source, "target" : elem.target, "label": elem.weight}
        counter = counter +1
    for node in all_nodes:
        nodes_list[node.id] = {"name" : node.name}

    graph = {"nodes" : nodes_list, "edges" : edges_list}
    return jsonify(graph)
    ##return jsonify(graph)

def create_adjacency_list(adj_list):
    all_edges = edges.query.all()
    for elem in all_edges:
        adj_list[elem.source].append([elem.target, elem.weight])

@api.route('/get_undirected_shortest_path', methods=['GET'])
def get_undirected_shortest_path():
    adjacency_list = defaultdict(list)
    create_adjacency_list(adjacency_list)

    list = {}

    return "DONE"