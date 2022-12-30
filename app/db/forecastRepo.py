from app.config.db import get_db
from werkzeug.local import LocalProxy

db = LocalProxy(get_db)


def getTempBetweenTwoDates(first,second):
    print(first,second)
     
    return db.temp_pred.find({
        "date":{
            '$gte':  first,
            '$lt': second
            } 
        })

def getWeatherBetweenTwoDates(first,second):
    #print(first,second)
     
    temp = db.temp_pred.find({
        "date":{
            '$gte':  first,
            '$lt': second
            } 
        })

    hum = db.huminidy_pred.find({
        "date":{
            '$gte':  first,
            '$lt': second
            } 
        })



    solar = db.solar_pred.find({
        "date":{
            '$gte':  first,
            '$lt': second
            } 
        })

    return [list(temp),list(hum),list(solar)]
    
    


def insertTemp(data,data1,data2):
    print(data)
    db.temp_pred.insert_many(data1)
    db.huminidy_pred.insert_many(data)
    db.solar_pred.insert_many(data2)

def insertCSV(data):
    db.to_pred.insert_many(data)


def insertTempMany(data,data1,data2):
    print(data)
    db.temp_pred.insert_many(data1)
    db.huminidy_pred.insert_many(data)
    db.solar_pred.insert_many(data2)


def getCurrentWeather(date):

    pipeline = [
            {
                "$match": {
                    "date":date
                }
            }
        ]
    try:
        temp = db.temp_pred.aggregate(pipeline).next()
        #dew = db.dewpoint_pred.aggregate(pipeline).next()
        hum =db.huminidy_pred.aggregate(pipeline).next()
        solar =db.solar_pred.aggregate(pipeline).next()

        return [temp, hum, solar]
     
    except:
        return None

def getLastSevenDaysTemperature():

    return db.to_pred.find({})


def getLastDaysTemperaturePredicted():
    temp_data = db.temp_pred.find({})
    hum_data = db.huminidy_pred.find({})
    solar_data = db.solar_pred.find({})

    return [temp_data,hum_data,solar_data]