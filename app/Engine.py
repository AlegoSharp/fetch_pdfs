import time
from flask import  jsonify

from Fetcher import Fetcher
from Scraper import Scraper
fetcher = Fetcher()

def fetch_all_raa(annee):
    res = []
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

    for departement in departements:
        res.append({
            "departement" : departement,
            "datas": fetch_departement_raa(departement, annee)
        })
        time.sleep(5)
    return res

def fetch_departement_raa(departement, annee):
    fetcher.tor_get_new_id()

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
        "Actes Administratifs",
        "Arrêtés préfectoraux"
    ])

    # Workaround si on ne trouve pas l'url des RAA directement
    #     Départements conercnés : jura, alpes-de-haute-provence
    if len(raa_urls) == 0:
        raa_urls = scraper.get_raa_urls([
            "Publications légales",
            "Publications administratives et légales",
        ])
        # Si on trouve une des pages concernées on navigue vers la page pour continuer
        if len(raa_urls) > 0:
            page = fetcher.get_page(raa_urls[0],"get")
            scraper = Scraper(base_url, page.content)

            raa_urls = scraper.get_raa_urls([
                "RAA",  
                "actes administratifs",
                "Actes Administratifs",
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
            return {
                'publications': full_url,
                'raa_url':  raa_urls,
                'subpage_urls':  subPage_urls,
                'links': pdfs
            }
        
        # Pas de page pour chaque mois
        pdfs.append({
            'subpage_url': subPage_url,
            'pdfs': scraper.get_pdfs()
        })

    
    return {
        'publications': full_url,
        'raa_url':  raa_urls,
        'subPage_urls':  subPage_urls,
        'links': pdfs
    }