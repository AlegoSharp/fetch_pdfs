import re
import requests 
import PyPDF2 

def readPdf(body_json:any):
    headers = {"User-Agent": "yyyy"}
    response = requests.get(body_json['url'], headers=headers)

    with open('/tmp/raa.pdf', 'wb') as f:
        f.write(response.content)

    reader = PyPDF2.PdfReader("/tmp/raa.pdf")

    # define key terms
    string = "rassemblements festifs à caractère musical"
    match = False
    pagesFound = []
    # extract text and do the search
    for index, page in enumerate(reader.pages):
        text = page.extract_text() 
        res_search = re.search(string, text)
        if res_search:
            pagesFound.append(index)
            match = True
        
    return {
        "match":match,
        "pages":pagesFound
    }