#!/usr/bin/python
# -*- coding: utf-8 -*-
import bs4, re, requests,sys

from pollution import pollutionReport
#from contacts import addressBook
from contacTest import addressBook
from mailer import sendMail

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

def windDiscDirection (windDirStr):
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
##def windDiscDirection (windDirStr):
##    windDir = int(windDirStr)
##    if windDir >= 338 or windDir <= 22:
##        return 'N'
##    elif windDir >= 23 and windDir <= 67:
##        return 'NE'
##    elif windDir >= 68 and windDir <= 112:
##        return 'E'
##    elif windDir >= 113 and windDir <= 157:
##        return 'SE'
##    elif windDir >= 158 and windDir <= 202:
##        return 'S'
##    elif windDir >= 203 and windDir <= 247:
##        return 'SW'
##    elif windDir >= 248 and windDir <= 292:
##        return 'W'
##    elif windDir >= 293 and windDir <= 337:
##        return 'NW'

#TODO: def precipNumericParser


def hello(name):
    return "Dzień dobry, "+name+"!"


def current (generic, tempFeelNow, pressNow, cloudNow, rainNow, snowNow, windSpeedNow, windDirNow, humidNow):
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

    desc = "Aktualnie w Krakowie jest "+generic+", a temperatura to "+tempFeelNow+". "+windStrength+" "
    return desc

def forecasted (tempFeel, press, cloud, rain, snow, windSpeed, windDir):
    windDisc = windDiscDirection(windDir)

    desc = "W ciągu dnia temperatura odczuwalna wyniesie "+tempFeel+", zaś ciśnienie "+press+ \
    ". Niebo będzie zachmurzone w "+cloud+", a spadnie z niego w ciągu doby "+str(rain)+ \
    " mm deszczu oraz "+str(snow)+" mm śniegu. Wiatr w kierunku "+windDisc+" będzie wiał z prędkością "+str(windSpeed)+" km\h. "

    return desc


def sunTime (sunrise, sunset):
    sun = "Słońce wschodzi o godzinie "+sunrise+", a zachodzi o "+sunset+". "
    return sun


def bye():
    return "Miłego dnia! :) \n\n--\nby MZ\ndane: Onet/GIOŚ"
 


res = requests.get('https://pogoda.onet.pl/prognoza-pogody/dlugoterminowa/krakow-306020')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

generic = soup.select('#wts_p0 div[class="forecastDesc"]')[0].getText().replace('\n','').replace('\t','').replace('\r','').lower()
now = soup.select('#wts_p0 li')
forecast = soup.select('#wtl_p0 li')
sun = soup.select('#wtl_p0 div span[class="text"] strong')


degRegEx = re.compile('(\d\d|\d\d\d)deg')
speedRegEx = re.compile('(\d|\d\d|\d\d\d) km')
precipRegEx = re.compile('((\d|\d\d),(\d)) mm')


tempFeelNow = now[0].select('span[class="restParamValue"]')[0].getText()
rainRawNow = now[1].select('span[class="restParamValue"]')[0].getText()
rainNow = float(precipRegEx.search(rainRawNow).group(1).replace(',','.'))
cloudNow = now[2].select('span[class="restParamValue"]')[0].getText()

windSpeedRawNow = now[3].select('span[class="restParamValue"]')[0].getText()[0:7]
windSpeedNow = float(speedRegEx.search(str(windSpeedRawNow)).group(1))
windDirRawNow = now[3].select('span[class="windDirectionArrow"]')
windDirNow = degRegEx.search(str(windDirRawNow)).group(1)

snowRawNow = now[4].select('span[class="restParamValue"]')[0].getText()
snowNow = float(precipRegEx.search(snowRawNow).group(1).replace(',','.'))

pressNow = now[5].select('span[class="restParamValue"]')[0].getText()
humidNow = now[6].select('span[class="restParamValue"]')[0].getText()


for i in range(len(forecast)):
    if forecast[i].select('span[class="restParamLabel"]')[0].getText()=="T. odczuw.":
        tempFeel = forecast[i].select('span[class="restParamValue"]')[0].getText()
    elif forecast[i].select('span[class="restParamLabel"]')[0].getText()=="Deszcz":
        rainRaw = forecast[i].select('span[class="restParamValue"]')[0].getText()
        rain = float(precipRegEx.search(rainRaw).group(1).replace(',','.'))
    elif forecast[i].select('span[class="restParamLabel"]')[0].getText()=="Zachm.":
        cloud = forecast[i].select('span[class="restParamValue"]')[0].getText()
    elif forecast[i].select('span[class="restParamLabel"]')[0].getText()=="Wiatr":
        windSpeedRaw = forecast[i].select('span[class="restParamValue"]')[0].getText()[0:7]
        windSpeed = float(speedRegEx.search(str(windSpeedRaw)).group(1))
        windDirRaw = forecast[i].select('span[class="windDirectionArrow"]')
        windDir = degRegEx.search(str(windDirRaw)).group(1)
    elif forecast[i].select('span[class="restParamLabel"]')[0].getText()[1:]=="nieg":
        snowRaw = forecast[i].select('span[class="restParamValue"]')[0].getText()
        snow = float(precipRegEx.search(snowRaw).group(1).replace(',','.'))
    elif forecast[i].select('span[class="restParamLabel"]')[0].getText()[3:]=="nienie":
        press = forecast[i].select('span[class="restParamValue"]')[0].getText()

sunrise = sun[0].getText()
sunset = sun[1].getText()


for name in addressBook:
    desc = hello(name) +"\n\n"+\
       current(generic, tempFeelNow, pressNow, cloudNow, rainNow, snowNow, windSpeedNow, windDirNow, humidNow) +"\n\n"+\
       forecasted(tempFeel, press, cloud, rain, snow, windSpeed, windDir) +"\n"+\
       sunTime(sunrise, sunset) +"\n\n"+\
       pollutionReport() +"\n\n"+\
       bye()
    recipient = addressBook[name]
    sendMail(desc.encode('utf-8'), recipient)
