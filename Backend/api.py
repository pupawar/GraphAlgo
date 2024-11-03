
from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/create_directed_graph')
def create_directed_grap():
    