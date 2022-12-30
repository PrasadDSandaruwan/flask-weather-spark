
from operator import ge
from flask import Blueprint, request, jsonify
from flask_cors import CORS

from app.utility.jwt import authentication 


from app.services.userService import addUserService, loginService
from app.db.dashboardRepo import getWeather, getYearMonthAvg, getSummerSolarBubbleList, getWinterSolarBubbleList, getAutumnSolarBubbleList, getSpringSolarBubbleList

user_route = Blueprint(
    'user_route', 'user_route', url_prefix='/api/v1/user')

CORS(user_route)

@user_route.route("/add-user",methods=["POST"])
@authentication
def addUser():
    post_data = request.get_json()
    try:
        first_name = post_data.get('first_name')
        last_name = post_data.get('last_name')
        email = post_data.get('email')
        password = post_data.get('password')


        addUserService(first_name,last_name,email,password)

        return jsonify({
            "success": "Successfully added."
        }),200
           
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_route.route("/login",methods=["POST"])
def login():
    print("LOGIN")
    post_data = request.get_json()
    try:
        email = post_data.get('email')
        password = post_data.get('password')

        return loginService(email,password)


         
    except Exception as e:
        print("ERROR", e)
        return jsonify({'error': str(e)}), 400


@user_route.route("/weather",methods=["GET"])
def getData():
    return getWeather()

@user_route.route("/yearmonthavg",methods=["GET"])
def getData1():
    return getYearMonthAvg()

@user_route.route("/summersolarbubble",methods=["GET"])
def getData2():
    return getSummerSolarBubbleList()

@user_route.route("/wintersolarbubble",methods=["GET"])
def getData3():
    return getWinterSolarBubbleList()

@user_route.route("/springsolarbubble",methods=["GET"])
def getData4():
    return getSpringSolarBubbleList()

@user_route.route("/autumnsolarbubble",methods=["GET"])
def getData5():
    return getAutumnSolarBubbleList()


