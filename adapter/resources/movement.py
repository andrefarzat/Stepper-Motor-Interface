# encoding: utf-8

from flask_restful import Resource, reqparse
from flask import jsonify, abort
from util.request_wrapper import post_data, get_data
import util.endpoint as endpoint
import util.helper as helper

class SingleAxisMove(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('direction', type = str, required = True, help = helper.MOVE['direction'], location = 'json')
		self.reqparse.add_argument('steps', type = int, required = True, help = helper.MOVE['steps'], location = 'json')
		self.reqparse.add_argument('acquisition_rate', type = int, required = True, help = helper.MOVE['acquisition_rate'], location = 'json')
		super(SingleAxisMove, self).__init__()

	def post(self, axis):
		axis_list = {"x": 4, "y": 3, "z": 1}
		
		if axis in axis_list:
			args = self.reqparse.parse_args()
			acquisition_rate = args['acquisition_rate']
			full_path = args['steps']

			response_list = []

			for i in range(0, full_path, acquisition_rate):
				data = {	'direction': args['direction'], 'steps': acquisition_rate, 'acknowledge': True 	}
				response = post_data(endpoint.movement + "/{}".format(axis_list.get(axis)), data)
				
				response_node = str(response.json()['response'])

				if response_node == "ao" or response_node == "a":
					acquired_data = get_data(endpoint.acquire).json()
					print("Obtendo ponto: %s" % i)
					response_list.append(acquired_data or "SCOPE LINE ERROR")
				else: 
					response_list.append("MOTOR RESPONSE ERROR")

			return {'message': response_list}, 200
		else:
			abort(400)

class MultipleAxisMove(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('x_axis', type = bool, required = False, location = 'json')
		self.reqparse.add_argument('y_axis', type = bool, required = False, location = 'json')
		self.reqparse.add_argument('z_axis', type = bool, required = False, location = 'json')
		self.reqparse.add_argument('direction_list', required = True, help = helper.MOVE['direction'], action='append')
		self.reqparse.add_argument('steps_list', required = True, help = helper.MOVE['steps'], action='append')
		super(MultipleAxisMove, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()
		data = {	
					"axis": 2, 
					"motor_number_list": ["1", "3", "4"], 
					"direction_list": ["f", "f", "f"], 
					"steps_list": [50, 50, 50], 
					"acknowledge": true
				}

		return post_data(endpoint.movement)