import sys
import requests
import csv
from bs4 import BeautifulSoup as BS
ODDELOVAC = 80*"-"

print(ODDELOVAC)
print(
"""Volby do Poslanecké sněmovny Parlamentu České republiky 
konané ve dnech 20.10. – 21.10.2017 (promítnuto usnesení NSS).
Data z webu VOLBY.CZ""")
print(ODDELOVAC)
if len(sys.argv) < 3:
  print(
    """Nedostatecny pocet argumentu (skript pozaduje 2 argumenty, tj. nazev uzemniho celku
(okresniho mesta) a nazev vystupniho souboru. Ukoncuji...""")
  quit()
elif len(sys.argv) > 3:
  argv3 = "_".join(sys.argv[2:])
  sys.argv.append(argv3)
  output = str(sys.argv[-1])
else:
  output = str(sys.argv[2])

input = (str(sys.argv[1])).title()

### overeni spravnosti formatu pro nazev vystupu zadaneho uzivatelem

output_sep02 = output.split(".")
if output_sep02[-1] != "csv":
  output_sep02.append("csv")
  output = ".".join(output_sep02)

print(f"Nazev vystupniho souboru: '{output}'. Pokracuji...")
print("")
print(f"Hledam data pro uzemni celek {input}...")
print("")

def get_soup(url):
  r = requests.get(url)
  return  BS(r.text, 'html.parser')

base_url = "https://volby.cz/pls/ps2017nss/"
url_level_1 = base_url + "ps3?xjazyk=CZ"
soup = get_soup(url_level_1)

### vyhledani vsech obci (uzemnich celku, tj. okresu) a overeni spravnosti vstupu od uzivatele
okresy_nazvy = []
for i in range(1,15):
  okresy_td = soup.find_all("td", {"headers": f"t{i}sa1 t{i}sb2"})
  for okres in okresy_td:
    okresy_nazvy.append((okres.string).title())

if input in okresy_nazvy:
  print(f"Stahuji data pro uzemni celek {input}...")
else:
  print("Uzemni celek nenalezen, ukoncuji...")
  quit()
print("")

### vyhledani prislusneho td na zaklade vstupu od uzivatele --> v next siblings vyhledani odkazu na detail okresu
for i in range(1,15):
  okres_td = soup.find("td", {"headers": f"t{i}sa1 t{i}sb2",}, "WHATEVER", f"{input}")
  if okres_td != None:
    break
url_level_2 = base_url + okres_td.find_next_sibling("td", {"class": "center", "headers": f"t{i}sa3"}).a["href"]

### prochazim url vybraneho okresu
soup2 = get_soup(url_level_2)

urls_level_3 = []
kody_obci = []
nazvy_obci = []

### a ziskavam kody obci, nazvy vsech obci a jim prislusne odkazy
obce_td_cislo = soup2.find_all("td", {"class": "cislo"})
for td in obce_td_cislo:
  url_level_3 = td.a["href"]
  kod_obce = td.string
  urls_level_3.append(base_url + url_level_3)
  kody_obci.append(kod_obce)
# print(urls_level_3)
# print(kody_obci)

obce_td_name = soup2.find_all("td", {"class": "overflow_name"})
for td in obce_td_name:
  nazev_obce = td.string
  nazvy_obci.append(nazev_obce)
# print(nazvy_obci)

################################################################
### ziskavani dat pro tabulku ze stranek jednotlivych obci
################################################################

hlavicka = ["kod obce", "nazev obce", "pocet opravnenych volicu", "pocet vydanych obalek", "platne hlasy"]

## strany do hlavicky ziskam z prvni obce, pro volby do PS jsou kandidatky pro kraj jednotne
strany_td = get_soup(urls_level_3[0]).find_all("td", {"class": "overflow_name"})
strany = []
for td in strany_td:
  strana =td.string
  strany.append(strana)
  hlavicka.append(strana)
# print(strany)
# print(hlavicka)

## vyhledani zisku stran a dalsich parametru a tvorba listu pro tabulku --> zapis do csv
f = open(output, mode="w")
f_writer = csv.writer(f)
f_writer.writerow(hlavicka)

for i,url in enumerate(urls_level_3):
  soup = get_soup(url)

  zisky_stran = []
  zisky_stran_td = soup.find_all("td", {"class": "cislo", "headers": f"t1sa2 t1sb3"}) + soup.find_all("td", {"class": "cislo", "headers": f"t2sa2 t2sb3"})

  for td in zisky_stran_td:
    zisk =(td.string).replace("\xa0", " ")
    # zisk = zisk.replace("\xa0", " ")
    zisky_stran.append(zisk)
  # print(zisky_stran)

  volici = (soup.find("td", {"class": "cislo", "headers": "sa2"}).string).replace("\xa0", " ")
  obalky = (soup.find("td", {"class": "cislo", "headers": "sa3"}).string).replace("\xa0", " ")
  platne_hlasy = (soup.find("td", {"class": "cislo", "headers": "sa6"}).string).replace("\xa0", " ")

  # print(volici)
  # print(obalky)
  # print(platne_hlasy)

  row = []
  row.append(kody_obci[i])
  row.append(nazvy_obci[i])
  row.append(volici)
  row.append(obalky)
  row.append(platne_hlasy)
  row = row + zisky_stran

  f_writer.writerow(row)


f.close()

print(f"Data byla stazena a ulozena do souboru: '{output}' ")