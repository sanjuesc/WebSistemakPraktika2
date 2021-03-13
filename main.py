# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import urllib

import requests


cookie=""

def login():
    global cookie
    atera = False
    metodoa = 'POST'
    datuak= ""
    uneko_uria= "https://egela.ehu.eus"

    while not atera:
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(datuak)), "Cookie" : cookie}
        erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
        print(erantzuna.status_code)
        atera = (erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" not in str(erantzuna.content))
        if "Location" in erantzuna.headers:
            uneko_uria=erantzuna.headers['Location']
        if "Set-Cookie" in erantzuna.headers:
            cookie = erantzuna.headers['Set-Cookie']
        if(erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" in str(erantzuna.content)):
            datuak = {'username': "aqui va tu ldap", 'password':'aqui tu pass.'}
        print(erantzuna.content)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    login()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
