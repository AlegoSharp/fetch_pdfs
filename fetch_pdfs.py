import requests
from bs4 import BeautifulSoup
import re

departements = [
    "ain", "aisne", "allier", "alpes-de-haute-provence", "hautes-alpes",
    "alpes-maritimes", "ardeche", "ardennes", "ariege", "aube",
    "aude", "aveyron", "bouches-du-rhone", "calvados", "cantal",
    "charente", "charente-maritime", "cher", "correze", "corse-du-sud",
    "haute-corse", "cote-dor", "cotes-darmor", "creuse", "dordogne",
    "doubs", "drome", "eure", "eure-et-loir", "finistere",
    "gard", "haute-garonne", "gers", "gironde", "ille-et-vilaine",
    "indre", "indre-et-loire", "isere", "jura", "landes",
    "loir-et-cher", "loire", "haute-loire", "loire-atlantique", "loiret",
    "lot", "lot-et-garonne", "lozere", "maine-et-loire", "manche",
    "marne", "haute-marne", "mayenne", "meurthe-et-moselle", "meuse",
    "morbihan", "moselle", "nievre", "nord", "oise",
    "orne", "pas-de-calais", "puy-de-dome", "pyrenees-atlantiques", "hautes-pyrenees",
    "pyrenees-orientales", "bas-rhin", "haut-rhin", "rhone", "haute-saone",
    "saone-et-loire", "sarthe", "savoie", "haute-savoie", "prefecturedepolice.interieur",
    "seine-maritime", "seine-et-marne", "yvelines", "deux-sevres", "somme",
    "tarn", "tarn-et-garonne", "var", "vaucluse", "vendee",
    "vienne", "haute-vienne", "vosges", "yonne", "territoire de belfort",
    "essonne", "hauts-de-seine", "seine-saint-denis", "val-de-marne", "val-doise",
    "guadeloupe", "martinique", "guyane", "reunion", "mayotte"
]

keywords = [
    "RAA",
    "actes administratifs"
]

print(f'departement;status;raa_url')
for departement in departements:
    raa_url=""
    status = "error"
    
    # Replace this with the URL for the desired year
    base_url = f'https://www.{departement}.gouv.fr'
    full_url = f'{base_url}/Publications/'

    headers = {'User-Agent': 'whatever'}
    # Send an HTTP request to the URL
    response = requests.get(full_url, headers=headers)

    text = "actes"
    for keyword in keywords:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        tag = soup.find('a', string=re.compile(text))# Print the PDF links

        if tag is not None:
            raa_url = tag['href']

        if raa_url is not None and raa_url != "":
            status = "OK"
    print(f'{departement};{status};{base_url}{raa_url}')
    #print(" ")
    #print(" ")
    #print("================================")

#the_word = 'actes administratifs'
#tags = soup.find_all('a', string=the_word)
#print(response.content)
## Find all the links to the PDF files
##pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
#
## Print the PDF links
#for link in tags:
#    #print(f'https://www.finistere.gouv.fr{link}')
#    print(f'{link}')