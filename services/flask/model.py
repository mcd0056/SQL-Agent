from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    response_text = db.Column(db.String, nullable=False)
    keyword = db.Column(db.String, nullable=False)
