import json
import os
import uuid
from datetime import datetime, timezone, date

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, abort, reqparse
from mongoengine import Document, EmailField, IntField, StringField, DateTimeField, ReferenceField, NotUniqueError, \
    ValidationError
# Obtenemos la variable de entorno
from werkzeug.exceptions import NotFound, BadRequest

API_HOST = os.environ.get('API_HOST', 'localhost')
DB_HOST = os.environ.get('DB_HOST', '')
DB_NAME = os.environ.get('DB_NAME', '')
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

# Configuracion app
app = Flask(__name__)
api = Api(app)

# Configuracion db
db = MongoEngine()

app.config['MONGODB_SETTINGS'] = {
    'host': DB_HOST,
    'db': DB_NAME,
    'connect': False,
    'username': DB_USER,
    'password': DB_PASSWORD,
    'authentication_source': 'admin'
}

db.init_app(app)


# Creacion Modelos db


class User(Document):
    email = EmailField(required=True)
    name = StringField(max_length=255, required=True)
    surname = StringField(max_length=255, required=True)


class Measurement(Document):
    sys = IntField(min_value=0, max_value=200, required=True)
    dia = IntField(min_value=0, max_value=200, required=True)
    pul = IntField(min_value=0, max_value=200, required=True)
    created = DateTimeField(default=date.today, unique=True)
    user = ReferenceField(User, required=True)

    def to_dic(self):
        return {
            'id': str(self.id),
            'sys': self.sys,
            'dia': self.dia,
            'pul': self.pul,
            'created': self.created.strftime("%Y-%m-%d"),
            'user': str(self.user.id)
        }


# Simulacion base de datos


def generate_uuid():
    identifier = uuid.uuid4()
    return json.dumps(identifier, default=str)


def get_utc_now():
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    return json.dumps(now, default=str)


MEASUREMENTS = [
    {
        'id': '490aa6e856ccf208a054389e47ce0d06',
        'sys': 120,
        'dia': 88,
        'pul': 70,
        'created': get_utc_now(),
        'user_id': '8f9bfe9d1345237cb3b2b205864da075'
    },
    {
        'id': '474ae52625b87d7628ae7b20a',
        'sys': 170,
        'dia': 90,
        'pul': 70,
        'created': get_utc_now(),
        'user_id': '9f8a2389a20ca0752aa9e9509351'
    }
]


# class measurement(Resource):
#
#     def get(self, id):
#
#         # import pdb #Debugger
#         # pdb.set_trace() # debugger
#
#         for measurement in MEASUREMENTS:
#             print('id: ', id)
#             print('var: ', measurement.get('id'))
#             if id == measurement.get('id'):
#                 return measurement, 200
#         abort(
#             404,
#             message={
#                 'message': 'Measurement ID={id} was not found'
#             }
#         )

class MeasurementDetail(Resource):
    def get(self, id):
        try:
            measurement = Measurement.objects(id=id).first()
            if measurement is not None:
                return measurement.to_dic(), 200
            abort(404, message=f'Measurement ID={id} was not found')
        except NotFound as e:
            raise e
        except Exception as e:
            abort(500, message=str(e))


class MeasurementList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sys', type=int, required=True, location='json')
        self.reqparse.add_argument('dia', type=int, required=True, location='json')
        self.reqparse.add_argument('pul', type=int, required=True, location='json')
        super(MeasurementList, self).__init__()

    def get(self):
        import pdb;
        pdb.set_trace()
        try:
            data = [measurement.to_dic() for measurement in Measurement.objects]
            return data, 200
        except Exception as e:
            abort(500, message=str(e))

    def post(self):
        try:
            data = self.reqparse.parse_args()
            measurement = Measurement(**data)
            user = User.objects(email='darkklitos@gmail.com').first()
            measurement.user = user
            measurement.save()
            return measurement.to_dic(), 201

        except BadRequest as e:
            abort(400, message=e.data.get('message'))
        except(NotUniqueError, ValidationError)as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))

        # def get(self):
        #     return MEASUREMENTS, 200
        #
        # def post(self):
        #     data = json.loads(request.data)
        #     measurement = {
        #         'id': ge nerate_uuid(),
        #         'sys': data.get('sys'),
        #         'dia': data.get('dia'),
        #         'pul': data.get('pul'),
        #         'created': get_utc_now(),
        #         'user_id': '8f9bfe9d1345237cb3b2b205864da075'
        #     }
        #     MEASUREMENTS.append(measurement)
        #     return measurement, 201


# api.add_resource(measurement, '/v1/measurements/<string:id>')
api.add_resource(MeasurementDetail, '/v1/measurements/<string:id>')
api.add_resource(MeasurementList, '/v1/measurements/')

if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    # ya no se necesita porque se toman los del archivo .env
    app.run(host=API_HOST)
