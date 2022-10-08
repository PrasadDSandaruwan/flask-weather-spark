from urllib import response
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from datetime import datetime


# from app.config.db import addUser


route_test = Blueprint(
    'route_test', 'route_test', url_prefix='/api/v1/')

CORS(route_test)

@route_test.route('/test', methods=['GET'])
def api_test_get():
  
    return jsonify({
        "Message":"Success"
    }),200



