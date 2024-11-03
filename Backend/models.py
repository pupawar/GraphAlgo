from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class nodes(db.Model):
    __tablename__ = "nodes"
    id = db.Column(db.Integer(), primary_key=True)
    name =  db.Column(db.String(10), nullable=False)

class edges(db.Model):
    __tablename__ = "edges"
    source = db.Column(db.Integer(), db.ForeignKey('nodes.id'), primary_key=True)
    target = db.Column(db.Integer(), db.ForeignKey('nodes.id'), primary_key=True)
    __table_args__ =(
        db.PrimaryKeyConstraint('source', 'target'),

    )

