# ElectionsScrapper_PJ
Web scraper vysledku voleb do PS roku 2017.

PRED SPUSTENIM NUTNO NAINSTALOVAT POTREBNE KNIHOVNY
Muzes tak ucinit pomoci souboru requirements.txt a prikazem do konsole:
"pip install -r requirements.txt"
(pripadne "pip3 install -r requirements.txt")

Skript stahne data o volbach pro vybrany uzemni celek a ulozi je do souboru csv.
Skript se spousti z konsole a potrebuje 2 argumenty:
  1) Nazev okresniho mesta (uzemniho celku), jehoz data chceme zpracovavat a ulozit
  2) Nazev vystupniho souboru
Pokud zadame (na prvni pozici) neexistujici nazev obce, resp. nazev NE okresniho mesta/ uzemniho celku, skript nas upozorni a ukonci se.
Pokud zadame vic nez 2 argumenty (napr. slova v nazvu vystupu oddelime mezerou), skript nadbytecne argumenty spoji do nazvu vystupu.

Ukazka funkce:

python3  ElectionsScrapper.py tŘEBÍČ volby 2017

--------------------------------------------------------------------------------
Volby do Poslanecké sněmovny Parlamentu České republiky
konané ve dnech 20.10. – 21.10.2017 (promítnuto usnesení NSS).
Data z webu VOLBY.CZ
--------------------------------------------------------------------------------
Nazev vystupniho souboru: 'volby_2017.csv'. Pokracuji...

Hledam data pro uzemni celek Třebíč...

Stahuji data pro uzemni celek Třebíč...

Data byla stazena a ulozena do souboru: 'volby_2017.csv'
