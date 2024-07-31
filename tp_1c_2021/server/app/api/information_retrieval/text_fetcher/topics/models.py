from app import db


class TextTopic(db.Model):
    topic = db.Column(db.String, primary_key=True)
