from app.config.db import get_db
from werkzeug.local import LocalProxy
from flask import jsonify
# from bson.json_util import dumps
# import json
import pandas as pd

db = LocalProxy(get_db)

def getWeather():
    d = db.weatherdata.find({})
    # d = db.weatherdata.find_one()
    # d.pop('_id')
    # return dumps(list(d),indent = 2)[1]
    df = pd.json_normalize(d)
    dfyear = pd.DataFrame(df.groupby(['year'])['temperature'].mean())
    year = dfyear.index.to_list()
    temp = dfyear['temperature'].to_list()
    result = {}
    result['year'] = year
    result['temp'] = temp
    # dfyear['year'] = dfyear.index
    # avgtemp = json.loads(json.dumps(list(dfyear.T.to_dict().values())))
    # return jsonify(list(d))
    return jsonify(result)

def getYearMonthAvg():
    d = db.yearmonthaverage.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('year-month')
    result = {}
    result['yearmonth'] = df['year-month'].to_list()
    result['temp'] = df['temperature'].to_list()
    result['dewpt'] = df['dewpoint_temperature'].to_list()
    result['wind'] = df['wind_speed'].to_list()
    result['pressure'] = df['mean_sea_level_pressure'].to_list()
    result['relhum'] = df['relative_humidity'].to_list()
    result['solar'] = df['surface_solar_radiation'].to_list()
    result['thermal'] = df['surface_thermal_radiation'].to_list()
    return jsonify(result)

def getSummerSolarBubbleList():
    # d = db.summersolarbubble.find({})
    # df = pd.json_normalize(d)
    # print(df.columns)
    df = pd.read_csv('E:/My Semester 5/Data Science and Engineering Project/flask-weather-spark/app/datasets/summerhrsolar.csv')
    df = df.sort_values('hour')
    result = {}
    for i in range(2016,2021):
        sub = df[['yr'+str(i),'hour']]
        sub.rename(columns = {'hour':'x', 'yr'+str(i):'y'}, inplace = True)
        sub['r'] = sub['y']//20
        sub['r'].replace(0, 2,inplace=True)
        sub['r'].replace(1, 2,inplace=True)
        lis = sub.to_dict(orient='records')
        result[i] = lis
    return jsonify(result)

def getWinterSolarBubbleList():
    # d = db.wintersolarbubble.find({})
    # df = pd.json_normalize(d)
    # print(df.columns)
    df = pd.read_csv('E:/My Semester 5/Data Science and Engineering Project/flask-weather-spark/app/datasets/winterhrsolar.csv')
    df = df.sort_values('hour')
    result = {}
    for i in range(2016,2021):
        sub = df[['yr'+str(i),'hour']]
        sub.rename(columns = {'hour':'x', 'yr'+str(i):'y'}, inplace = True)
        sub['r'] = sub['y']//20
        sub['r'].replace(0, 2,inplace=True)
        sub['r'].replace(1, 2,inplace=True)
        lis = sub.to_dict(orient='records')
        result[i] = lis
    return jsonify(result)

def getAutumnSolarBubbleList():
    # d = db.autumnsolarbubble.find({})
    # df = pd.json_normalize(d)
    # print(df.columns)
    df = pd.read_csv('E:/My Semester 5/Data Science and Engineering Project/flask-weather-spark/app/datasets/autumnhrsolar.csv')
    df = df.sort_values('hour')
    result = {}
    for i in range(2016,2021):
        sub = df[['yr'+str(i),'hour']]
        sub.rename(columns = {'hour':'x', 'yr'+str(i):'y'}, inplace = True)
        sub['r'] = sub['y']//20
        sub['r'].replace(0, 2,inplace=True)
        sub['r'].replace(1, 2,inplace=True)
        lis = sub.to_dict(orient='records')
        result[i] = lis
    return jsonify(result)

def getSpringSolarBubbleList():
    # d = db.springsolarbubble.find({})
    # df = pd.json_normalize(d)
    # print(df.columns)
    df = pd.read_csv('E:/My Semester 5/Data Science and Engineering Project/flask-weather-spark/app/datasets/springhrsolar.csv')
    df = df.sort_values('hour')
    result = {}
    for i in range(2016,2021):
        sub = df[['yr'+str(i),'hour']]
        sub.rename(columns = {'hour':'x', 'yr'+str(i):'y'}, inplace = True)
        sub['r'] = sub['y']//20
        sub['r'].replace(0, 2,inplace=True)
        sub['r'].replace(1, 2,inplace=True)
        lis = sub.to_dict(orient='records')
        result[i] = lis
    return jsonify(result)