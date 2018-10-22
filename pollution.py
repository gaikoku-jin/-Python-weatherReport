#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, bs4, requests


def pollutionReport():

        res2 = requests.get('http://powietrze.gios.gov.pl/pjp/current/station_details/table/400/1/0')
        res2.raise_for_status()
        soup2 = bs4.BeautifulSoup(res2.text, "lxml")

        pol_6 = soup2.select('tr')[6]

        pm10_6 = pol_6.select('td')[0].getText().replace(',','.')
        pm10_6float = float(pm10_6)
        pm10_6Norm = str(float(pm10_6)*2)

        pm25_6 = pol_6.select('td')[1].getText().replace(',','.')
        pm25_6float = float(pm25_6)
        pm25_6Norm = str(float(pm25_6)*4)


        polDesc = "Na Alei Krasińskiego stężenie pyłu PM10 wynosi "+str(pm10_6float)+ \
        " µg/m3, co stanowi "+pm10_6Norm+"% normy,"+ \
        " zaś stężenie pyłu PM2.5 wynosi "+str(pm25_6float)+ \
        " µg/m3, co stanowi "+pm25_6Norm+"% normy."

        return polDesc
