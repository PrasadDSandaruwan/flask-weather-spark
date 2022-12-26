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

    dew = db.dewpoint_pred.find({
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

    return [temp,dew,hum,solar]
    
    


def insertTemp(data,data1,data2):
    print(data)
    db.dewpoint_pred.insert_one(data1)
    db.huminidy_pred.insert_one(data)
    db.solar_pred.insert_one(data2)

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
        dew = db.dewpoint_pred.aggregate(pipeline).next()
        hum =db.huminidy_pred.aggregate(pipeline).next()
        solar =db.solar_pred.aggregate(pipeline).next()

        return [temp,dew, hum, solar]
     
    except:
        return None

