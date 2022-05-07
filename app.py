import requests
import json
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)

from models import *

CORS(app)


def get_api_question():
    r = requests.get('https://jservice.io/api/random?count=1')
    r = r.json()
    try:
        exists = db.session.query(DbQuestion.id).filter_by(id=int(r[0]['id'])).first() is not None
        
        if not exists:
            new_q = DbQuestion(r[0]['id'], r[0]['answer'], r[0]['question'])
            db.session.add(new_q)
            db.session.commit()
            db.session.close()
        else:
            get_api_question()
    except Exception as e:
        print(e)
    


def get_db_question():
    question = DbQuestion.query.order_by(desc(DbQuestion.created)).first()
    return question


class Question(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('questions_num')
        args = parser.parse_args()
        try:
            q_count = int(args['questions_num'])
            for count in range(q_count):
                get_api_question()
            db_obj = get_db_question()
            if not db_obj:
                return {}
            nq = {
                'id': db_obj.id,
                'text_question': db_obj.text_question,
                'text_answer': db_obj.text_answer,
                'created': (db_obj.created + datetime.timedelta(hours=3)).strftime('%d/%m/%Y %H:%m:%S'),
            }
            return {"question": nq}

        except ValueError:
            message = f'Invalid argument \'{args["questions_num"]}\'. Only number allowed!'
            return {"error": message}
    


api.add_resource(Question, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
