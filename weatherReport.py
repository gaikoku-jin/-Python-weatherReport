#!/usr/bin/python
# -*- coding: utf-8 -*-
import bs4, re, requests,sys
from datetime import datetime
from pprint import pprint as pp
from statistics import mean

from pollution import pollutionReport
from contacts import addressBook
from contacts import linkTuple
# from contacts import locativeBook
# from mailer import sendMail

if sys.version[0] == '2':
    # reload(sys)
    sys.setdefaultencoding("utf-8")

if len(sys.argv) > 1:
    # parameter = bytes(sys.argv[1].encode())
    apiCode = str(sys.argv[1]) # chwilowo 1, potem 2 jak wejdzie klucz

def windDiscDirection(windDirStr):
    windDir = int(windDirStr)
    if windDir >= 338 or windDir <= 22:
        return 'północnym'
    elif windDir >= 23 and windDir <= 67:
        return 'północno-wschodnim'
    elif windDir >= 68 and windDir <= 112:
        return 'wschodnim'
    elif windDir >= 113 and windDir <= 157:
        return 'południowo-wschodnim'
    elif windDir >= 158 and windDir <= 202:
        return 'południowym'
    elif windDir >= 203 and windDir <= 247:
        return 'południowo-zachodnim'
    elif windDir >= 248 and windDir <= 292:
        return 'zachodnim'
    elif windDir >= 293 and windDir <= 337:
        return 'północno-zachodnim'


def hello(name):
    return "Dzień dobry, "+name+"!\n\n"


def current (generic, tempFeelNow, pressNow, cloudNow, rainNow, snowNow, windSpeedNow, windDirNow, locative):
    windDiscNow = windDiscDirection(windDirNow)

    if (rainNow==0 and snowNow==0):
        precip = "Brak opadów."
    elif (rainNow>0 and snowNow==0):
        precip = "Pada deszcz ("+str(rainNow)+" mm/24h)."
    elif (rainNow==0 and snowNow>0):
        precip = "Śnieży!"
    else:
        precip = "Możliwy deszcz ze śniegiem."

    if (windSpeedNow==0):
        windStrength = "Jest bezwietrznie."
    elif (windSpeedNow<10):
        windStrength = "Odczuwalny delikatny wietrzyk ("+str(windSpeedNow)+" km\h)."
    elif (windSpeedNow<30):
        windStrength = "Umiarkowane podmuchy wiatru ("+str(windSpeedNow)+" km\h)."
    elif (windSpeedNow<70):
        windStrength = "Wieje mocny wiatr ("+str(windSpeedNow)+" km\h)."
    else:
        windStrength = "Szaleje wichura ("+str(windSpeedNow)+" km\h)!"

    desc = "Aktualnie w "+locative+" jest "+generic+", a temperatura odczuwalna to "+ \
           str(tempFeelNow)+"℃. "+windStrength+"\n\n"

    return desc

def forecasted (tempMax, tempMin, press, cloud, rain, snow, windSpeed, windDir):
    windDisc = windDiscDirection(windDir)

    desc = "W ciągu dnia temperatura maksymalna wyniesie "+str(tempMax)+"℃, a minimalna "+str(tempMin)+ \
           "℃, zaś ciśnienie "+str(press)+" hPa. Niebo będzie zachmurzone w "+str(cloud)+ \
           "%, a spadnie z niego w ciągu doby "+str(rain)+" mm deszczu oraz "+str(snow)+ \
           " mm śniegu. Wiatr w kierunku "+str(windDisc)+" powieje z predkoscia "+str(windSpeed)+" km\h. \n"

    return desc


def sunTime (sunrise, sunset):
    return "Słońce wschodzi o godzinie "+sunrise+", a zachodzi o "+sunset+". \n\n"


def bye():
    return "\n\nMiłego dnia! :) \n\n--\nby MZ\ndane: OpenWeatherMap/GIOŚ"
 

for city in addressBook:
    currentJson, forecastJson = linkTuple(city, apiCode)
    res = requests.get(currentJson)
    res.raise_for_status()
    now = res.json()

    generic = now["weather"][0]["description"]
    loc = addressBook[city]["locative"]

    tempFeelNow = float('%.1f' % ((now["main"]["temp"])-273.15))
    rainNow = 0
    cloudNow = now["clouds"]["all"]

    windSpeedNow = float('%.1f' % now["wind"]["speed"])
    windDirNow = float(now["wind"]["deg"])

    snowNow = 0

    pressNow = now["main"]["pressure"]

    sunriseTimeStamp = float(now["sys"]["sunrise"])
    sunrise = datetime.fromtimestamp(sunriseTimeStamp).strftime("%H:%M")

    sunsetTimeStamp = float(now["sys"]["sunset"])
    sunset = datetime.fromtimestamp(sunsetTimeStamp).strftime("%H:%M")

    res2 = requests.get(forecastJson)
    res2.raise_for_status()
    forecast = res2.json()

    tempMax = float('%.1f' % (max([forecast["list"][i]["main"]["temp_max"] for i in range(0, 4)])-273.15))
    tempMin = float('%.1f' % (min([forecast["list"][i]["main"]["temp_min"] for i in range(0, 4)])-273.15))
    press = int(mean([forecast["list"][i]["main"]["pressure"] for i in range(0, 4)]))
    cloud = int(mean([forecast["list"][i]["clouds"]["all"] for i in range(0, 8)]))
    # rain = sum([forecast["list"][i]["rain"]["3h"] for i in range(0,8)])
    rain = 0
    # snow = mean([forecast["list"][i]["snow"]["3h"] for i in range(0,8)])
    snow = 0
    windSpeed = max([forecast["list"][i]["wind"]["speed"] for i in range(0, 8)])
    windDir = mean([forecast["list"][i]["wind"]["deg"] for i in range(0, 4)])

    currentWeather = current(generic, tempFeelNow, pressNow, cloudNow, rainNow, snowNow, windSpeedNow, windDirNow, loc)
    forecastWeather = forecasted(tempMax, tempMin, press, cloud, rain, snow, windSpeed, windDir)
    sun = sunTime(sunrise, sunset)
    pollution = pollutionReport(city)


    for name in addressBook[city]["names"]:
        helloMessage = hello(name)
        byeMessage = bye()

        desc = helloMessage + \
            currentWeather + \
            forecastWeather + \
            sun + \
            pollution + \
            byeMessage

        recipient = addressBook[city]["names"][name]
        pp(desc)
        pp(recipient)
        pp("")
    # sendMail(desc.encode('utf-8'), recipient, parameter)
