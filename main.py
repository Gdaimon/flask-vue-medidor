import json
import uuid
from datetime import datetime, timezone

from flask import Flask, request
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

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


class measurement(Resource):

    def get(self, id):

        for measurement in MEASUREMENTS:
            print('id: ', id)
            print('var: ', measurement.get('id'))
            if id == measurement.get('id'):
                return measurement, 200
        abort(
            404,
            message={
                'message': 'Measurement ID={id} was not found'
            }
        )


class MeasurementList(Resource):
    def get(self):
        return MEASUREMENTS, 200

    def post(self):
        data = json.loads(request.data)
        measurement = {
            'id': generate_uuid(),
            'sys': data.get('sys'),
            'dia': data.get('dia'),
            'pul': data.get('pul'),
            'created': get_utc_now(),
            'user_id': '8f9bfe9d1345237cb3b2b205864da075'
        }
        MEASUREMENTS.append(measurement)
        return measurement, 201


api.add_resource(measurement, '/v1/measurements/<string:id>')
api.add_resource(MeasurementList, '/v1/measurements/')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
