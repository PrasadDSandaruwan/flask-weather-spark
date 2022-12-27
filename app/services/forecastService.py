from pytz import timezone
from datetime import datetime
from datetime import timedelta

from app.db.forecastRepo import getTempBetweenTwoDates,getCurrentWeather, getWeatherBetweenTwoDates, insertCSV



"""
in date format 3 has to change for -%d
if lenth != given condition, model have to predict the value and
    store in the database

"""

def getMinMaxTemp():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)

    now = now.strftime("%Y-%m-3 00:00:00")
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    one_day = now+timedelta( days=1)

    one_day = one_day.strftime("%Y-%m-%d 00:00:00")
    one_day = datetime.strptime(one_day,"%Y-%m-%d %H:%M:%S")

    cur= getTempBetweenTwoDates(now,one_day)
    cur= list(cur)

    if len(cur)== 24:
        result=[]

        for doc in cur:
            result.append(doc["temperature"])

        

        res = {
            "Min": min(result),
            "Max": max(result),
            "Avg": round(sum(result)/len(result),2)
        }

        return res

    else:
        return "EROROR"



def getWeatherNowService():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)
    now = now.strftime("%Y-%m-3 %H:00:00")
    #print(now)
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    #print(now)

    results = getCurrentWeather(now)

    #print(results)
    res= {
        "temperature": round(results[0]["temperature"],2),
        "dewpoint_temp": round(results[1]["dewpoint_temp"],2),
        "huminidy": round(results[2]["huminidy"],2),
        "solar_radiation": round(results[3]["solar_radiation"],2),
        "time":now.strftime("%I:00 %p"),
        "date": now.strftime("%Y-%m-%d")
    }
    #print(res)
    return res

def getWeekDaysNames():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)
    now = now.strftime("%Y-%m-3 00:00:00")
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    res=[]
    for i in range(7):
        new_date = now+timedelta(days=i)
        res.append({new_date.strftime("%A"): new_date.strftime("%b %d")})
    return res




def getNextSevenDaysPrediction():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)

    now = now.strftime("%Y-%m-3 00:00:00")
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    seven_days = now+timedelta( days=1)

    seven_days = seven_days.strftime("%Y-%m-%d 00:00:00")
    seven_days = datetime.strptime(seven_days,"%Y-%m-%d %H:%M:%S")

    results = getWeatherBetweenTwoDates(now,seven_days)

    res = {}

    c=0
    for data in results:
        data = list(data)

        if c==0:
            res["dates"] = [ i["date"].strftime("%H-%M")   for i in data]
            c+=1

        k = data[0].keys()
        key=""
        for i in k:
            if i!="_id" and i!="date":
                key=i
                break
        res[key]= [i[key] for i in data]
    
    return res


def updateToPredictData(data):
    insertCSV(data)

        

        
    

        










    

