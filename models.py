import datetime
from sqlalchemy.sql import func
from app import db


class DbQuestion(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text_question = db.Column(db.Text)
    text_answer = db.Column(db.Text)
    created = db.Column(db.DateTime, default=func.now())

    def __init__(self, question_id, text_question, text_answer, **kwargs):
        super(DbQuestion, self).__init__(**kwargs)
        self.id = question_id
        self.text_question = text_question
        self.text_answer = text_answer

    def __repr__(self):
        return self.id
