# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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
        atera = (erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" not in str(erantzuna.content))
        if ("Location" in erantzuna.headers and erantzuna.status_code == 303): ## berbideraketa egin
            print(uneko_uria + " hurrengo orria eramango gaitu "+ erantzuna.headers['Location'] )
            uneko_uria=erantzuna.headers['Location']
        if "Set-Cookie" in erantzuna.headers: ## cookiea gorde
            cookie = erantzuna.headers["Set-Cookie"].split(';')[0] #soilik cookie berria interesatzen zaigu, ezabatzen dena ez
        if(erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" in str(erantzuna.content)):
            izena = str(input("Sartu zure LDAP\t"))
            pasahitza = str(input("Sartu zure pasahitza\t")) ##begiratu behar dut pasahitza kontsolan ez ikusteko zer egin
            datuak = {'username': izena , 'password': pasahitza}
    ondo = "ANDER SAN JUAN" in str(erantzuna.content)
    if(ondo):
        print("Login-a ondo egin da")

# Press the green button in the gutter to run the script.
def pdfDeskargatu():
    metodoa = 'POST'
    datuak= ""
    uneko_uria= "https://egela.ehu.eus/course/view.php?id=42336"
    goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(datuak)), "Cookie" : cookie}
    erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
    print(str(erantzuna.status_code) +" "+ uneko_uria)

if __name__ == '__main__':
    login()
    pdfDeskargatu()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
