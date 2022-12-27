from flask import Blueprint, request, jsonify
from flask_cors import CORS


from app.utility.jwt import authentication 
from app.services.forecastService import getMinMaxTemp,getWeatherNowService,getNextSevenDaysPrediction,getWeekDaysNames, updateToPredictData,getTemperturePrediction
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
    


@forecast_route.route("/upload-csv",methods=["POST"])
def uploadCSV():
    f = request.files["file"]
   
    # file1 = open(f, 'r')
    Lines = f.readlines()
    headers = str(Lines[0],'utf-8').rstrip().split(",")

    columns = ['temperature',
     'dewpoint_temperature',
      'wind_speed', 'mean_sea_level_pressure',
       'relative_humidity', 'surface_solar_radiation',
        'surface_thermal_radiation', 'total_cloud_cover',
         'timestamp']

    dataset = []   
    data_indexs={}
    data_2={}
    
    for i in range(len(columns)):
        print(columns[i])
        if columns[i] not in headers:
            return jsonify({"data" :"Headers are missing."}),201
        data_indexs[columns[i]]=i
        data_2[columns[i]]=[]
    print(data_2)
    for line in Lines[1:]:
        line=str(line,'utf-8')
        line= line.rstrip().split(",")
        data = data_2.copy()
        for i in columns:
            if i == "timestamp":
               data[i]= datetime.strptime(line[data_indexs[i]],"%d/%m/%Y %H:%M")
            else:
                data[i]= line[data_indexs[i]]
        dataset.append(data)
    #print(dataset)
    updateToPredictData(dataset)

    return jsonify({"data" :"OK"}),200


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
    


@forecast_route.route("/data",methods=["GET"])
def check():
    getTemperturePrediction()
    return jsonify({"data" :"OK"}),200