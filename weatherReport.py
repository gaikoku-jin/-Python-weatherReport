#!/usr/bin/python
# -*- coding: utf-8 -*-
import bs4, re, requests

from pollution import pollutionReport
from contacts import addressBook
from mailer import sendMail


def windDiscDirection (windDirStr):
    windDir = int(windDirStr)
    if windDir >= 338 or windDir <= 22:
        return 'N'
    elif windDir >= 23 and windDir <= 67:
        return 'NE'
    elif windDir >= 68 and windDir <= 112:
        return 'E'
    elif windDir >= 113 and windDir <= 157:
        return 'SE'
    elif windDir >= 158 and windDir <= 202:
        return 'S'
    elif windDir >= 203 and windDir <= 247:
        return 'SW'
    elif windDir >= 248 and windDir <= 292:
        return 'W'
    elif windDir >= 293 and windDir <= 337:
        return 'NE'


def description (name, tempFeel, press, cloud, rain, snow, windSpeed, windDir):
    windDisc = windDiscDirection(windDir)
    
    desc = "Dzień dobry, "+name+"! \n\nDzisiejsza temperatura odczuwalna w Krakowie wyniesie "+tempFeel+ \
    ", zaś ciśnienie "+press+". Niebo będzie zachmurzone w "+cloud+", a spadnie z niego w ciągu doby "+ \
    rain+" deszczu oraz "+snow+" śniegu. Wiatr w kierunku "+windDisc+" będzie wiał z prędkością "+windSpeed+ \
    ". \n\n"+pollutionReport()+" \n\nMiłego dnia! :) \n _ _\nby MZ\ndane: Onet/GIOŚ"
    return desc
  

res = requests.get('https://pogoda.onet.pl/prognoza-pogody/dlugoterminowa/krakow-306020')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

li = soup.select('#wtl_p0 li')


degRegEx = re.compile('(\d\d|\d\d\d)deg')


for i in range(len(li)):
    if li[i].select('span[class="restParamLabel"]')[0].getText()=="T. odczuw.":
        tempFeel = li[i].select('span[class="restParamValue"]')[0].getText()
    elif li[i].select('span[class="restParamLabel"]')[0].getText()=="Deszcz":
        rain = li[i].select('span[class="restParamValue"]')[0].getText()
    elif li[i].select('span[class="restParamLabel"]')[0].getText()=="Zachm.":
        cloud = li[i].select('span[class="restParamValue"]')[0].getText()
    elif li[i].select('span[class="restParamLabel"]')[0].getText()=="Wiatr":
        windSpeed = li[i].select('span[class="restParamValue"]')[0].getText()[0:7]
        windDirRaw = li[i].select('span[class="windDirectionArrow"]')
        windDir = degRegEx.search(str(windDirRaw)).group(1)
    elif li[i].select('span[class="restParamLabel"]')[0].getText()[1:]=="nieg":
        snow = li[i].select('span[class="restParamValue"]')[0].getText()
    elif li[i].select('span[class="restParamLabel"]')[0].getText()[3:]=="nienie":
        press = li[i].select('span[class="restParamValue"]')[0].getText()

for name in addressBook:
    desc = description(name, tempFeel, press, cloud, rain, snow, windSpeed, windDir)
    recipient = addressBook[name]
    sendMail(desc.encode('utf-8'), recipient)
