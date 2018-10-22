import re, bs4, requests

def pollution (pm10):
    polRegEx = re.compile('(\d|\d\d|\d\d\d) (.*)')
    pm10Val = polRegEx.search(pm10).group(1)
    pm10Norm = int(pm10Val)*2

    polDesc = "Stężenie pyłu PM10 wynosi na Alei Krasińskiego "+pm10Val+ \
              " µg/m3, co stanowi "+str(pm10Norm)+"% normy."
    return polDesc

res2 = requests.get('http://powietrzewkrakowie.pl/')
res2.raise_for_status()
soup2 = bs4.BeautifulSoup(res2.text, "lxml")


pm10 = soup2.select('td[class="right"]')[0].getText()

print(str(pm10))

print(pollution(pm10))
