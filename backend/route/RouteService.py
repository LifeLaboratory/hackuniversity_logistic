# coding=utf-8
from backend.api.helpers import base_errors as errors
from backend.api.helpers import base_name as names
from backend.api.helpers.service import Gis as gs
from flask_restful import Resource, reqparse
from backend.api.src.Authentication import auth
import json
from flask import jsonify
from flask import json


class Auth(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument(names.LOGIN)
        self.__parser.add_argument(names.PASSWORD)
        self.__args = self.__parser.parse_args()

    def parse_data(self):
        data = dict()
        data[names.LOGIN] = self.__args.get(names.LOGIN, None)
        data[names.PASSWORD] = self.__args.get(names.PASSWORD, None)
        return data

    def get(self):
        data = self.parse_data()
        answer = auth(data)
        return answer, 200, {'Access-Control-Allow-Origin': '*'}

    def option(self):
        return "OK", errors.OK, {'Access-Control-Allow-Origin': '*'}
