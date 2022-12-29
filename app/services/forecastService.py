from pytz import timezone
from datetime import datetime
from datetime import timedelta
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np

from app.db.forecastRepo import getTempBetweenTwoDates,getCurrentWeather, getWeatherBetweenTwoDates, insertCSV, getLastSevenDaysTemperature,insertTempMany,getLastDaysTemperaturePredicted



def getMinMaxTemp():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)

    now = now.strftime("2021-5-3 00:00:00")
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    one_day = now+timedelta( days=1)

    one_day = one_day.strftime("%Y-%m-%d 00:00:00")
    one_day = datetime.strptime(one_day,"%Y-%m-%d %H:%M:%S")

    cur= getTempBetweenTwoDates(now,one_day)
    cur= list(cur)

    if len(cur)!=24:
        getTemperturePrediction()
        cur= list(getTempBetweenTwoDates(now,one_day))


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
        return []



def getWeatherNowService():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)
    now = now.strftime("2021-5-3 %H:00:00")
    #print(now)
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    #print(now)

    results = getCurrentWeather(now)

    if len(list(results[0]))==0:
        getTemperturePrediction()
        results = getCurrentWeather(now)

        if len(list(results[0]))==0:
            return {}

    print(results)
    res= {
        "temperature": round(results[0]["temperature"],2),
        "huminidy": round(results[1]["huminidy"],2),
        "solar_radiation": round(results[2]["solar_radiation"],2),
        "time":now.strftime("%I:00 %p"),
        "date": now.strftime("%Y-%m-%d")
    }
    #print(res)
    return res

def getWeekDaysNames():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)
    now = now.strftime("2021-5-3 00:00:00")
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    res=[]
    for i in range(7):
        new_date = now+timedelta(days=i)
        res.append({new_date.strftime("%A"): new_date.strftime("%b %d")})
    return res




def getNextSevenDaysPrediction():
    t = timezone("Australia/Melbourne")
    now = datetime.now(t)

    now = now.strftime("2021-5-24 00:00:00")
    now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")

    seven_days = now+timedelta( days=7)

    seven_days = seven_days.strftime("%Y-%m-%d 00:00:00")
    seven_days = datetime.strptime(seven_days,"%Y-%m-%d %H:%M:%S")

    results = getWeatherBetweenTwoDates(now,seven_days)

    #print(results)

    if results[0]==None or len(results[0])==0 or len(results[0])!= 24*7:

        results = getTemperturePredictionWithForecast()
        # results = getWeatherBetweenTwoDates(now,seven_days)
        # if results[0]==None or len(results[0])==0:
        #     return {}


    res = {}


    c=0
    k = ["temperature","huminidy","solar_radiation"]
    i=0
    for data in results:
        
        #print(data)
        data = list(data)

        if c==0:
            res["dates"] = [ i["date"].strftime("%H-%M")   for i in data]
            c+=1

        k= data[0].keys()
        key=""
        for i in k:
            if i!="_id" and i!="date":
                key=i
                break
        #print(key)
        res[key]= [j[key] for j in data]
        
    
    return res

def getTemperturePredictionWithForecast():
    data = getLastDaysTemperaturePredicted()

    
    t_df = pd.json_normalize(data[0])
    h_df = pd.json_normalize(data[1])
    s_df = pd.json_normalize(data[2])

    #print(t_df)
    #print(h_df)

    df = pd.merge(t_df,h_df,on="date",how="inner")
    # df= t_df.merge(h_df,on="date")

    #print(df)
    df = pd.merge(df,s_df,on="date",how="inner")

    df= df.sort_values("date")
    #print(df)
    # print(df.head())
    # print(df.tail())
    df = df[-24*7:-24*6]

    # print(df.tail(7))

    
    #temperature
    temp_min = 0.8799999952316284
    temp_max =40.36000061035156
    temp_df =df[["temperature_y"]].astype("float32")
    temp_df["temperature_y"] = (temp_df["temperature_y"]-temp_min)/(temp_max-temp_min)
    to_pred = np.array([temp_df.temperature_y])
    to_pred = np.reshape(to_pred, (to_pred.shape[0], 1, to_pred.shape[1]))

    temp_model = load_model("app/model/temp_model.h5")

    pred = temp_model.predict(to_pred)[0]

    real_temp = []
    for i in pred:
        real_temp.append(i*(temp_max-temp_min)+ temp_min)


      #humidity
    temp_df =df[["huminidy_x"]].astype("float32")
    temp_df["huminidy_x"] = (temp_df["huminidy_x"]-temp_min)/(temp_max-temp_min)
    to_pred = np.array([temp_df.huminidy_x])
    to_pred = np.reshape(to_pred, (to_pred.shape[0], 1, to_pred.shape[1]))


    temp_model = load_model("app/model/huminidy.h5")

    real_humidity = temp_model.predict(to_pred)[0]



    
    #real_radiation 0.0 
    temp_min = 0
    temp_max =1103.9200439453125
    temp_df =df[["solar_radiation"]].astype("float32")
    temp_df["solar_radiation"] = (temp_df["solar_radiation"]-temp_min)/(temp_max-temp_min)
    to_pred = np.array([temp_df.solar_radiation])
    to_pred = np.reshape(to_pred, (to_pred.shape[0], 1, to_pred.shape[1]))


    temp_model = load_model("app/model/surface_solar_radiation.h5")

    pred = temp_model.predict(to_pred)[0]

    real_radiation = []
    for i in pred:
        real_radiation.append(i*(temp_max-temp_min)+ temp_min)
    
    date = list(df["date"])[-1]
    #print(list(df["timestamp"]))

    next_day = date + timedelta(1)

    next_day = next_day.strftime("%Y-%m-%d 00:00:00")
    next_day = datetime.strptime(next_day,"%Y-%m-%d %H:%M:%S")

    seven_days =  next_day+timedelta(7)

    

    dti = pd.date_range(next_day, seven_days, freq='H') # just specify hourly frequency...
    l = dti.to_list()[:-1]

    temp_prediction = []
    humidity_prediction =[]
    solar_prediction = []

    #print(l)

    for i in range(24*6,24*7):
        temp_prediction.append({
            "date":l[i],
            "temperature": float(real_temp[i])
        })

        humidity_prediction.append({
            "date":l[i],
            "huminidy": float(real_humidity[i])
        })

        solar_prediction.append({
            "date":l[i],
            "solar_radiation": float(real_radiation[i])
        })
    
    print(temp_prediction)



    return [temp_prediction,humidity_prediction,solar_prediction]

    #insertTempMany(temp_prediction,humidity_prediction,solar_prediction)



def updateToPredictData(data):
    insertCSV(data)
    getTemperturePrediction()

        
def getTemperturePrediction():
    data = getLastSevenDaysTemperature()
    df = pd.json_normalize(data)
    df= df.sort_values("timestamp")
    # print(df.head())
    # print(df.tail())
    df = df[-24:]

    # print(df.tail(7))

    
    #temperature
    temp_min = 0.8799999952316284
    temp_max =40.36000061035156
    temp_df =df[["temperature"]].astype("float32")
    temp_df["temperature"] = (temp_df["temperature"]-temp_min)/(temp_max-temp_min)
    to_pred = np.array([temp_df.temperature])
    to_pred = np.reshape(to_pred, (to_pred.shape[0], 1, to_pred.shape[1]))

    temp_model = load_model("app/model/temp_model.h5")

    pred = temp_model.predict(to_pred)[0]

    real_temp = []
    for i in pred:
        real_temp.append(i*(temp_max-temp_min)+ temp_min)


      #humidity
    temp_df =df[["relative_humidity"]].astype("float32")
    temp_df["relative_humidity"] = (temp_df["relative_humidity"]-temp_min)/(temp_max-temp_min)
    to_pred = np.array([temp_df.relative_humidity])
    to_pred = np.reshape(to_pred, (to_pred.shape[0], 1, to_pred.shape[1]))


    temp_model = load_model("app/model/huminidy.h5")

    real_humidity = temp_model.predict(to_pred)[0]



    
    #real_radiation 0.0 
    temp_min = 0
    temp_max =1103.9200439453125
    temp_df =df[["surface_solar_radiation"]].astype("float32")
    temp_df["surface_solar_radiation"] = (temp_df["surface_solar_radiation"]-temp_min)/(temp_max-temp_min)
    to_pred = np.array([temp_df.surface_solar_radiation])
    to_pred = np.reshape(to_pred, (to_pred.shape[0], 1, to_pred.shape[1]))


    temp_model = load_model("app/model/surface_solar_radiation.h5")

    pred = temp_model.predict(to_pred)[0]

    real_radiation = []
    for i in pred:
        real_radiation.append(i*(temp_max-temp_min)+ temp_min)
    
    date = list(df["timestamp"])[-1]
    #print(list(df["timestamp"]))

    next_day = date + timedelta(1)

    next_day = next_day.strftime("%Y-%m-%d 00:00:00")
    next_day = datetime.strptime(next_day,"%Y-%m-%d %H:%M:%S")

    seven_days =  next_day+timedelta(7)

    

    dti = pd.date_range(next_day, seven_days, freq='H') # just specify hourly frequency...
    l = dti.to_list()[:-1]

    temp_prediction = []
    humidity_prediction =[]
    solar_prediction = []

    #print(l)

    for i in range(24*6,24*7):
        temp_prediction.append({
            "date":l[i],
            "temperature": float(real_temp[i])
        })

        humidity_prediction.append({
            "date":l[i],
            "huminidy": float(real_humidity[i])
        })

        solar_prediction.append({
            "date":l[i],
            "solar_radiation": float(real_radiation[i])
        })
    
    #print(solar_prediction)

    insertTempMany(temp_prediction,humidity_prediction,solar_prediction)

    
    
        



        










    

