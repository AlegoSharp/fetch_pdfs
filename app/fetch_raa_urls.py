from bs4 import BeautifulSoup
import re
import time

from Scraper import Scraper

departements = [
    "finistere",
    "cotes-darmor",
    "morbihan",
    "ille-et-vilaine",
    "aube"
]

keywords = [
    "RAA",  
    "actes administratifs"
]

x = Scraper()

for departement in departements:
    base_url = f'https://www.{departement}.gouv.fr'
    full_url = f'{base_url}/Publications'
    raa_url = ""
    status = "NOK"
    res = x.get_page(full_url,"get")
    soup = BeautifulSoup(res.content, 'html.parser')

    for keyword in keywords:
        # Parse the HTML content of the page
        tag = soup.find('a', string=re.compile(keyword))# Print the PDF links

        if tag is not None:
            if tag['href'] is not None and tag['href'] != "":
                status = "OK"
                raa_url = tag['href']
                break
        
    print(f"{departement} : {status}  @ {base_url}{raa_url}")
    print(" ")