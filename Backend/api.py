
from flask import Blueprint, request
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

def create_adjacency_list():
    return

@api.route('/get_undirected_shortest_path', methods=['GET'])
def get_undirected_shortest_path():
