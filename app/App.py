from flask import Flask, jsonify, request
from Fetcher import Fetcher
from Scraper import Scraper

app = Flask(__name__)
app.json.sort_keys = False

fetcher = Fetcher()

@app.route('/api/<departement>/<annee>/pdfs', methods=['GET'])
def fetch_url(departement, annee):
    base_url = f'https://www.{departement}.gouv.fr'
    full_url = f'{base_url}/Publications'
    subPage_urls=[]
    pdfs=[]
    raa_urls = []

    """
    STEP 1 : Détection de la page racine RAA
    """ 
    page = fetcher.get_page(full_url,"get")
    scraper = Scraper(base_url, page.content)
    raa_urls = scraper.get_raa_urls([
        "RAA",  
        "actes administratifs",
        "Arrêtés préfectoraux"
    ])

    # Workaround si on ne trouve pas l'url des RAA directement
    #     Départements conercnés : jura
    if len(raa_urls) == 0:
        raa_urls = scraper.get_raa_urls([
            "Publications légales",
        ])
        # Si on trouve une des pages concernées on navigue vers la page pour continuer
        if len(raa_urls) > 0:
            page = fetcher.get_page(raa_urls[0],"get")
            scraper = Scraper(base_url, page.content)

            raa_urls = scraper.get_raa_urls([
                "RAA",  
                "actes administratifs",
                "Arrêtés préfectoraux"
            ])

    if len(raa_urls) == 0:
        return jsonify({
            'message': "Erreur, le programme ne peut pas analyser ce département",
            'détails': "Veuillez analyser le site et ajouter le texte du liens dans les 'keywords'",
            'url': full_url
        })
    
    """
    STEP 2 : Détection des sous pages années (ou paire années / mois)
    """ 
    page = fetcher.get_page(raa_urls[0], "get")
    scraper = Scraper(base_url, page.content)
    subPage_urls = scraper.get_raa_urls([
        f"RAA {annee}", 
        f"Recueil des actes administratifs {annee}", 
        f"Année {annee}", 
        f"{annee}"
    ])

    """
    STEP X : Récupération des liens de pdf
    """ 
    for subPage_url in subPage_urls:
        raas = fetcher.get_page(subPage_url,"get")
        scraper = Scraper(base_url, raas.content)
        months_raa = scraper.get_raa_urls([
            "Janvier",
            "Février",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Août",
            "Septembre",
            "Octobre",
            "Novembre",
            "Décembre",
        ], breakOnKeywords=False)

        # Si il y a des sous pages pour chaque mois
        if len(months_raa)> 0:
            for month_url in months_raa:
                month = fetcher.get_page(f'{month_url}',"get")
                scraper = Scraper(base_url, month.content)
                pdfs.append({
                    'subpage_url': month_url,
                    'pdfs': scraper.get_pdfs()
                })

            # Si les mois ont étés récupéré, on peut s'arrêter là vu qu'on filtre par années
            return jsonify({
                'publications': full_url,
                'raa_url':  raa_urls,
                'subpage_urls':  subPage_urls,
                'links': pdfs
            })
        
        # Pas de page pour chaque mois
        pdfs.append({
            'subpage_url': subPage_url,
            'pdfs': scraper.get_pdfs()
        })

    
    return jsonify({
        'publications': full_url,
        'raa_url':  raa_urls,
        'subPage_urls':  subPage_urls,
        'links': pdfs
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


""" 
Format 1 (29)   : /Publications/<keyword_raa>/<keyword_année>/
Format 2 (05)   : /Publications/<keyword_raa>/<keyword_année>/<keyword_mois>
Format 2 (XX)   : 


Format X (56)   : /Publications/<keyword_raa>/<keyword_année>/<keyword_mois>
"""