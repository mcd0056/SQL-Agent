from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PredefinedResponse(db.Model):
    __tablename__ = 'predefined_responses'

    id = db.Column(db.Integer, primary_key=True)
    response_text = db.Column(db.String, nullable=False)
    keyword = db.Column(db.String, nullable=False)
