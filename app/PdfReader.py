import re
import requests 
import PyPDF2 
import DbModels
import datetime
import dateparser

def readPdf(dpt:DbModels.Departement, url_pdf):
    url = f'https://www.{dpt.departement_slug}.gouv.fr{url_pdf}'

    headers = {"User-Agent": "yyyy"}
    response = requests.get(url, headers=headers)

    with open('/tmp/raa.pdf', 'wb') as f:
        f.write(response.content)

    reader = PyPDF2.PdfReader("/tmp/raa.pdf")

    # define key terms
    string = "rassemblements festifs à caractère musical"
    date_search = "du ((lundi|mardi|mercredi|jeudi|Vendredi|Samedi|Dimanche)(.+)au(.+)heures)"

    pdf_datas = {
        "pages_found":[],
        "start_date": "",
        "end_date": "",
        "match": False
    }    

    # extract text and do the search
    for index, page in enumerate(reader.pages):
        text = page.extract_text() 
        res_string_search = re.search(string, text)
        if res_string_search:
            pdf_datas["pages_found"].append(index)
            pdf_datas["match"] = True

        flat_text = text.replace("\n"," ").replace("\r","")
        res_date_search = re.search(date_search, flat_text, re.S)

        if res_date_search:
            date_match_parse = re.match(r"du (\w+ \d{2} \w+ \d{4}) .+ au (\w+ \d{2} \w+ \d{4})", res_date_search.group(0))
            pdf_datas["start_date"] = dateparser.parse(date_match_parse.group(1)).date()
            pdf_datas["end_date"] = dateparser.parse(date_match_parse.group(2)).date()

    return pdf_datas