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
    db.temp_pred.insert_one(data1)
    db.huminidy_pred.insert_one(data)
    db.solar_pred.insert_one(data2)

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

        return [list(temp), list(hum), list(solar)]
     
    except:
        return None

def getLastSevenDaysTemperature():
    pipeline = [
    
        {
            "$sort": { #stage 2: sort the remainder last-first
                "timestamp": -1
            }
        },
        {
            "$limit": 7 #stage 3: keep only 20 of the descending order subset
        },
        {
            "$sort": {
                "rt": 1 #stage 4: sort back to ascending order
            }
        },
        {
            "$project": { # stage 5: add any fields you want to show in your results
                "_id": 1,
                "timestamp" : 1,
                "temperature": 1
            }
        }
    ]
    return db.to_pred.find({})