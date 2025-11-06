import re
import requests 
import PyPDF2 
import DbModels
import datetime
import dateparser

def downloadPdf(url):

    headers = {"User-Agent": "yyyy"}
    response = requests.get(url, headers=headers)
    with open('/tmp/raa.pdf', 'wb') as f:
        f.write(response.content)

#def readPdfOCR(dpt:DbModels.Departement, url_pdf):
#    downloadPdf(dpt, url_pdf)
#
#    # convert to image using resolution 600 dpi 
#    pages = convert_from_path("/tmp/raa.pdf", 600)
#
#    # extract text
#    text_data = ''
#    for page in pages:
#        text = pytesseract.image_to_string(page)
#        text_data += text + '\n'
#    print(text_data)
    
def readPdf(dpt:DbModels.Departement, url_pdf):
    url = f'https://www.{dpt.departement_slug}.gouv.fr{url_pdf}'

    downloadPdf(url)
    pdf_datas = {
        "logs":[],
        "pages_found":[],
        "start_date": "",
        "end_date": "",
        "match": False,
        "pdf_url": url,
    }
    try:
        reader = PyPDF2.PdfReader("/tmp/raa.pdf")

        # define key terms
        keywords = [
            "rassemblements festifs à caractère musical", 
            "rassemblement festif",
            "rave-party",
            "free-party",
            "teknival",
            "sonorisation",
            "sound system",
            "diffusion de musique amplifiée",
        ]

        date_patterns = [
            r"((?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) \d+ \w+) au ((?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) \d+ \w+)", 
            r"((?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) \d+ \w+) (?:2025) à \d+ heures au ((?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) \d+ \w+) (?:2025)", 
            r"(\d{2} .+ )au( \d{2} .+)",
        ]


        # extract text and do the search
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if searchByKeywords(text, keywords):
                pdf_datas["pages_found"].append(index)
                pdf_datas["match"] = True

                flat_text = text.replace("\n"," ").replace("\r","")
                date_patterns_res = searchByKeywords(flat_text, date_patterns)
                if date_patterns_res:
                    pdf_datas["start_date"] = dateparser.parse(date_patterns_res.group(1)).date()
                    pdf_datas["end_date"] = dateparser.parse(date_patterns_res.group(2)).date()
    except:
        return pdf_datas

    return pdf_datas

def searchByKeywords(text, keywords):
    res={}
    for keyword in keywords:
        res = re.search(keyword, text)
        if res:
            return res
    return res
        
