import requests
import re
import os
import csv


#URL strani ljubljanskega maratona
lj_maraton_rezultati_url = "http://timingljubljana.si/lmzg/zgodovina_rez.asp?l=&lm=20lm&kat=42Z"
rezultati_directory = "rezultati"
frontpage_filename = "webpage.html"


def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
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
    '''Write "text" to the file "filename" located in directory "directory",
    creating "directory" if necessary. If "directory" is the empty string, use
    the current directory.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as file_out:
        file_out.write(text)
    return None

def save_maraton_webpage():
    webpage_text = download_url_to_string(lj_maraton_rezultati_url)
    save_string_to_file(webpage_text, rezultati_directory, frontpage_filename)
    return None



def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.
    '''
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        a = file_in.read()
        return a

def locitev_razdelkov():
    vsebina = read_file_to_string(rezultati_directory, frontpage_filename)
    vzorec = re.compile(r"<b>(\d+)<\/b>"  + r".*?" + r"<TD>([A-Z].+?)<\/TD>"
                        + r".*?" + r"nbsp;(\d{4}).nbsp"
                        + r".*?" + r"nbsp;((\d:\d{2}:\d{2})|(DNF))"
                        + r".*?" + r"nbsp;(\D)&nbsp"
                        + r".*?" + r"nbsp;(\d+)&nbsp"
                        ,  re.DOTALL)
    iterator = vzorec.finditer(vsebina)
    result = [x.group(8) for x in iterator]
    return result

print(locitev_razdelkov())