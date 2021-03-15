# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup

cookie = ""


def login():
    global cookie
    atera = False
    metodoa = 'POST'
    datuak = ""
    uneko_uria = "https://egela.ehu.eus"

    while not atera:
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": cookie}
        erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
        atera = (erantzuna.status_code == 200 and "ANDER SAN JUAN" in str(erantzuna.content))
        if (erantzuna.status_code == 303):  ## berbideraketa egin
            print(uneko_uria + " hurrengo orria eramango gaitu " + erantzuna.headers['Location'])
            uneko_uria = erantzuna.headers['Location']
        if "Set-Cookie" in erantzuna.headers:  ## cookiea gorde
            cookie = erantzuna.headers["Set-Cookie"].split(';')[
                0]  # soilik cookie berria interesatzen zaigu, ezabatzen dena ez
        if (erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" in str(erantzuna.content)):
            izena = str(input("Sartu zure LDAP\t"))
            pasahitza = str(
                input("Sartu zure pasahitza\t"))  ##begiratu behar dut pasahitza kontsolan ez ikusteko zer egin
            datuak = {'username': izena, 'password': pasahitza}
    print("Login-a ondo egin da")


# Press the green button in the gutter to run the script.
def jaitsiPDF(soup):
    uria=""
    guztiak = soup.find_all("div", {"class": "activityinstance"})
    for unekoPDF in guztiak:
        if unekoPDF.find("img", {"src": "https://egela.ehu.eus/theme/image.php/fordson/core/1611567512/f/pdf"}):
            uria = str(unekoPDF).split("onclick=\"window.open('")[1].split("\'")[0].replace("amp;","")
            filename = str(unekoPDF).split("view.php?")[1].split("\"")[0] + '.pdf'
            r = requests.get(uria, stream=True, allow_redirects=True)##esto no funca aun
            print(r.headers)
            print(r.status_code)
            #with open(filename, 'wb') as fd: #https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
            #    for chunk in r.iter_content():
            #        fd.write(chunk)



def lortuIkasgaia():
    metodoa = 'POST'
    datuak = ""
    uneko_uria = "https://egela.ehu.eus/course/view.php?id=42336"
    goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                 'Content-Length': str(len(datuak)), "Cookie": cookie}
    erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
    if (erantzuna.status_code == 200):
        print("Ikasgaiaren orria ondo lortu da")
        soup = BeautifulSoup(erantzuna.content, "html.parser")
        jaitsiPDF(soup)
    else:
        print("Orria ez da ondo lortu")


if __name__ == '__main__':
    login()
    lortuIkasgaia()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
