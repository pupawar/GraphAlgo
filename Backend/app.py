from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import quote_plus
from models import db, edges, nodes
from flask_cors import CORS
# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

import os

from api import api

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
DB_NAME = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':

    migrate.init_app(app,db)
    with app.app_context():
        try:
            
            db.create_all()
            print("Tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)
    
    app.register_blueprint(api, url_prefix='/api')
    app.run(debug=True);    
