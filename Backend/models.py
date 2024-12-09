from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class nodes(db.Model):
    __tablename__ = "nodes"
    id = db.Column(db.Integer(), primary_key=True)
    name =  db.Column(db.String(10), nullable=False)

class edges(db.Model):
    __tablename__ = "edges"
    id = db.Column(db.Integer(), primary_key=True)
    source = db.Column(db.Integer(), db.ForeignKey('nodes.id'), primary_key=True)
    target = db.Column(db.Integer(), db.ForeignKey('nodes.id'), primary_key=True)
    weight = db.Column(db.Integer())
    __table_args__ =(
        db.UniqueConstraint('source', 'target'),
    )

