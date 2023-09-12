import xmltodict
import csv
import fileinput
import requests
import os, shutil

#vnesi URL do XML povezave
url = ''
r = requests.get(url)

#odpri xml datoteko *
with open('*.xml', 'wb') as f:
    f.write(r.content)

# prebere xml datoteko
with open("*.xml") as file:
    filedata = file.read()
    
# pretvori xml v python dict    
data_dict = xmltodict.parse(filedata)

# naredi seznam parsed data
seznam_artiklov = [dict(x) for x in data_dict["podjetje"]["izdelki"]["izdelek"]]

# izbira naslovov celic za csv
HEADERS = ['Naziv', 'Opis', 'Slike', 'Redna cena', 'Zaloga', 'EAN' ,'sku']
rows = []

# indeksiranje csv
for izdelek in seznam_artiklov:
    izdelekIme = izdelek["izdelekIme"]
    Opis = izdelek["opis"]
    slikaVelika = izdelek["slikaVelika"]
    PPC = izdelek["PPC"]
    dobava = izdelek["dobava"]
    if dobava["#text"] == "ni na zalogi":
        dobava = 0
    else:
        dobava = 100
    if "EAN" in izdelek:
        EAN = izdelek["EAN"]
    else:
        EAN = ""
    sku = izdelek["sku"]

# dodajanje podatkov v csv
    rows.append([izdelekIme,Opis,slikaVelika,PPC,dobava,EAN,sku])

#pisanje csv
with open('store.csv', 'w',newline="", encoding='utf-8') as f:
    write = csv.writer(f)
    write.writerow(HEADERS)
    write.writerows(rows)

#sprememba stringov
with fileinput.FileInput("store.csv", inplace=True) as file:
    for line in file:
        print(line.replace('&scaron;', 'š'), end='')

#brisanje xml fajla
myfile = "*.xml"
#če datoteka obstaja jo brisi
if os.path.isfile(myfile):
    os.remove(myfile)
else:
    # ce ne moc brisati obvesti.
    print("Napaka: %s datoteka ne obstaja" % myfile)

#brisanje csv fajla
myfile = "store.csv"
# If file exists, delete it.
if os.path.isfile(myfile):
    os.remove(myfile)
else:
    # If it fails, inform the user.
    print("Napaka: %s datoteka ne obstaja" % myfile)
