import json
import os
import uuid
from datetime import datetime, timezone

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

from resources import MeasurementDetail, MeasurementList

# Obtenemos la variable de entorno

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


# Simulacion base de datos


def generate_uuid():
    identifier = uuid.uuid4()
    return json.dumps(identifier, default=str)


def get_utc_now():
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    return json.dumps(now, default=str)


api.add_resource(MeasurementDetail, '/v1/measurements/<string:id>')
api.add_resource(MeasurementList, '/v1/measurements/')

if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    # ya no se necesita porque se toman los del archivo .env
    app.run(host=API_HOST)
