import requests
import re
import os
import csv



#URL strani ljubljanskega maratona
vse_strani_lj_maraton = [("http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=19lm&kat=42M", 'podatki_moski19'),
                         ("http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=19lm&kat=42Z", 'podatki_zenske19'),
                          ("http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=20lm&kat=42M", 'podatki_moski20'),
                           ("http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=20lm&kat=42Z", 'podatki_zenske20'),
                            ("http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=21lm&kat=42M", 'podatki_moski21'),
                             ("http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=21lm&kat=42Z", 'podatki_zenske21')]
rezultati_directory = "rezultati"
frontpage_filename = "webpage.html"

def download_url_to_string(url):
    webpage = requests.get(url)
    webpage.encoding = "windows-1250"
    if webpage.ok:
        #no errors
        webpage_text = webpage.text
    else:
        #error
        webpage_text = "unable to get webpage"

    return webpage_text



def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as file_out:
        file_out.write(text)
    return None

def save_maraton_webpage(spletna_stran):
    webpage_text = download_url_to_string(spletna_stran)
    save_string_to_file(webpage_text, rezultati_directory, frontpage_filename)
    return None




def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        a = file_in.read()
        return a

def locitev_razdelkov():
    vsebina = read_file_to_string(rezultati_directory, frontpage_filename)
    vzorec = re.compile(r"<b>(?P<mesto>\d+)<\/b>"
                        + r".*?" + r"<TD>(?P<ime>[A-Z].+?)<\/TD>"
                        + r".*?" + r"nbsp;(?P<letnica_rojstva>\d{4}).nbsp"
                        + r".*?" + r"nbsp;(?P<drzava>\D{3})&nbsp"
                        + r".*?" + r"nbsp;(?P<netto_cas>(\d:\d{2}:\d{2})|(DNF))"
                        + r".*?" + r"nbsp;(?P<kategorija>\D)&nbsp"
                        + r".*?" + r"nbsp;(?P<mesto_v_kategoriji>\d+)&nbsp"
                        ,  re.DOTALL)
    iterator = vzorec.finditer(vsebina)
    result = [x.group('mesto', 'ime', 'letnica_rojstva', 'drzava', 'netto_cas', 'kategorija', 'mesto_v_kategoriji') for x in iterator]

    return result



def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)

polja = ['mesto', 'ime', 'letnica_rojstva', 'drzava', 'netto_cas', 'kategorija', 'mesto_v_kategoriji']

def zapisi_vse_csv(spletne_strani):
    for spletna_stran, ime_datoteke in spletne_strani:
        save_maraton_webpage(spletna_stran)
        podatki = locitev_razdelkov()
        koncni = []
        for sklop in podatki:
            novi_podatki = {}
            novi_podatki['mesto'] = sklop[0]
            novi_podatki['ime'] = sklop[1]
            novi_podatki['letnica_rojstva'] = sklop[2]
            novi_podatki['drzava'] = sklop[3]
            novi_podatki['netto_cas'] = sklop[4]
            novi_podatki['kategorija'] = sklop[5]
            novi_podatki['mesto_v_kategoriji'] = sklop[6]
            koncni.append(novi_podatki)
        zapisi_csv(koncni, polja, ime_datoteke)

zapisi_vse_csv(vse_strani_lj_maraton)
