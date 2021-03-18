import getpass

import requests
from bs4 import BeautifulSoup

cookie = ""


def login():
    global cookie
    metodoa = 'POST'
    datuak = ""
    uneko_uria = "https://egela.ehu.eus"
    eginda = False
    while not eginda: #loop batekin hasierako eskaerak egitea erabaki dut, bestela 5 aldiz ia kode berbera idatzi beharko nuke
        print("\n"+metodoa + " " +uneko_uria)
        if len(datuak)>0:
            print(datuak)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": cookie}
        erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
        eginda = (erantzuna.status_code == 200 and "ANDER SAN JUAN" in str(erantzuna.content))
        print(str(erantzuna.status_code) + " " + erantzuna.reason)
        if erantzuna.status_code == 303:  ## berbideraketa egin
            #print(uneko_uria + " hurrengo orria eramango gaitu " + erantzuna.headers['Location'])
            uneko_uria = erantzuna.headers['Location']
        if "Set-Cookie" in erantzuna.headers:  ## cookiea gorde
            cookie = erantzuna.headers["Set-Cookie"].split(';')[0]  # soilik cookie berria interesatzen zaigu, ezabatzen dena ez
        if erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" in str(erantzuna.content):
            izena = str(input("Sartu zure LDAP\t"))
            pasahitza = str(input("Sartu zure pasahitza\t"))  ##begiratu behar dut pasahitza kontsolan ez ikusteko zer egin
            datuak = {'username': izena, 'password': pasahitza}
        else:
            datuak={}
    print("Login-a ondo egin da")
    print("Azkenengo erantzunaren edukia: \n")
    print(erantzuna.content)
    return uneko_uria

def jaitsiPDF(soup):
    uria=""
    divGuztiak = soup.find_all("div", {"class": "activityinstance"})
    for unekoa in divGuztiak:
        if unekoa.find("img", {"src": "https://egela.ehu.eus/theme/image.php/fordson/core/1611567512/f/pdf"}): #egelako elementuetatik, pdf bezala agertzen direnak bilatu
            uria = str(unekoa).split("onclick=\"window.open('")[1].split("\'")[0].replace("amp;","")
            metodoa = 'POST'
            datuak = ""
            goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                             'Content-Length': str(len(datuak)), "Cookie": cookie}
            erantzuna = requests.request(metodoa, uria, data=datuak, headers=goiburuak, allow_redirects=False)
            pdfURI= erantzuna.headers['Location']
            erantzuna = requests.request(metodoa, pdfURI, data=datuak, headers=goiburuak, allow_redirects=False)
            filename = pdfURI.split("mod_resource/content/")[1].split("/")[1].replace("%20", "_") #fitxategiaren izena ondo ikusteko
            with open(filename, 'wb') as fd: #  https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
                for chunk in erantzuna.iter_content():
                    fd.write(chunk)



def lortuIkasgaia(uneko_uria):
    metodoa = 'POST'
    datuak = ""
    goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                 'Content-Length': str(len(datuak)), "Cookie": cookie}
    erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
    soup = BeautifulSoup(erantzuna.content, "html.parser")
    ikasgaiak = soup.find_all("a", {"class": "ehu-visible"})
    for x in ikasgaiak:
        if("Web Sistemak" in x):
            uneko_uria=x["href"]
            break

    erantzuna = requests.request(metodoa, uneko_uria, data=datuak, headers=goiburuak, allow_redirects=False)
    if (erantzuna.status_code == 200):
        print("Ikasgaiaren orria ondo lortu da")
        soup = BeautifulSoup(erantzuna.content, "html.parser")
        jaitsiPDF(soup)
    else:
        print("Orria ez da ondo lortu")


if __name__ == '__main__':
    egelaOrria=login()
    lortuIkasgaia(egelaOrria)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
