#!/usr/bin/python
# -*- coding: utf-8 -*-


# addressBook = {"Kraków": {"Zakrzew":"marcin.zakrzewski@koliber.org"}, "Gorlice":{"Marcin":"xz13033@shibaura-it.ac.jp"}}

#linkBook = {"Gorlice":"https://pogoda.onet.pl/prognoza-pogody/dlugoterminowa/gorlice-289471","Kraków":"https://pogoda.onet.pl/prognoza-pogody/dlugoterminowa/krakow-306020"}

# codeBook = {"Gorlice":"Gorlice,pl","Kraków":"Krakow,pl","Oslo":"Oslo,no"}

def linkTuple (city, apiCode):
    return ["http://api.openweathermap.org/data/2.5/"+infoKind+"?q="+addressBook[city]["code"]+"+&APPID="+apiCode+"&lang=pl" for infoKind in ("weather","forecast")]

# locativeBook = {"Gorlice":"Gorlicach","Kraków":"Krakowie"}



addressBook = {
    "Kraków":{
        "code" : "Krakow,pl",
        "locative" : "Krakowie",
        "names" :{
            "Zakrzew" : "marcin.zakrzewski@koliber.org",
            "Kasia" : "slys.kasia@gmail.com"
        }
    },
    "Gorlice":{
        "code" : "Gorlice,pl",
        "locative" : "Gorlicach",
        "names" :{
            "Marcin" : "xz13033@shibaura-it.ac.jp",
            "Madzia" : "gamad@op.pl",
        }
    },
    "Oslo":{
        "code" : "Oslo,no",
        "locative" : "Oslo",
        "names" :{
            "Asia":"joanna.zakrzewska.br@gmail.com"
        }
    }
}