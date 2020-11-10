from flask_restful import Resource, abort, reqparse
from mongoengine import NotUniqueError, \
    ValidationError
# Obtenemos la variable de entorno
from werkzeug.exceptions import NotFound, BadRequest

from models import Measurement, User
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
from utils import normalize_data, get_formatted_date, get_today_date


class MeasurementDetail(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sys', type=int, required=False, location='json')
        self.reqparse.add_argument('dia', type=int, required=False, location='json')
        self.reqparse.add_argument('pul', type=int, required=False, location='json')
        super(MeasurementDetail, self).__init__()

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

    def patch(self, id):
        try:
            import pdb
            pdb.set_trace()
            measurement = Measurement.objects(id=id).first()
            if measurement is not None:
                if get_formatted_date(measurement.created) != get_formatted_date(get_today_date()):
                    raise BadRequest(f'Cannot update a measurement for {measurement.created}')
                data = self.reqparse.parse_args()
                data = normalize_data(data)  # eliminamos los valores None
                measurement.update(**data)
                measurement.reload()
                return measurement.to_dic(), 200
            abort(404, message=f'Measurement ID={id} was not found')
        except BadRequest as e:
            raise e
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
        import pdb
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
