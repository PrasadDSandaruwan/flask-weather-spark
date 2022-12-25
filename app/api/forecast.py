from flask import Blueprint, request, jsonify
from flask_cors import CORS


from app.utility.jwt import authentication 
from app.services.forecastService import getMinMaxTemp,getWeatherNowService,getNextSevenDaysPrediction,getWeekDaysNames
from app.db.forecastRepo import insertTemp

from datetime import datetime

forecast_route = Blueprint(
    'forecast_route', 'forecast_route', url_prefix='/api/v1/forecast')

CORS(forecast_route)


@forecast_route.route("/min-max",methods=["GET"])
def getMinMaxTemperature():
    
    return jsonify({"data" :getMinMaxTemp()}),200


@forecast_route.route("/weather-now", methods=["GET"])
def getWeatherNow():
    return jsonify(getWeatherNowService()),200

@forecast_route.route("/next-seven-days", methods=["GET"])
def getNextSevenDays():
    return jsonify(getNextSevenDaysPrediction()),200

@forecast_route.route("/weekdays", methods=["GET"])
def getWeekDays():
    return jsonify(getWeekDaysNames()),200
    






@forecast_route.route("/insert",methods=["GET"])
def insertPred():
    file1 = open('app\model\predicted.csv', 'r')
    Lines = file1.readlines()
    
    for line in Lines[1:]:
        line= line.rstrip().split(",")

        data={
            "date":datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S"),
            "huminidy": round(float(line[1]),2)
        }
        data1={
            "date":datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S"),
            "dewpoint_temp": round(float(line[1]),2)*2
        }
        data2={
            "date":datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S"),
            "solar_radiation": round(float(line[1]),2)*3
        }
        insertTemp(data,data1,data2)
    return jsonify({"data" :"OK"}),200
    

