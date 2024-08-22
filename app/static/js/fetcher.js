// Fonction pour effectuer une requête HTTP GET et récupérer le contenu de la page
function getPage(url) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    resolve(xhr.responseText);
                } else {
                    reject(`Error fetching ${url}: ${xhr.statusText}`);
                }
            }
        };
        xhr.send();
    });
}

// Fonction pour extraire les URLs des RAA à partir de la page HTML
function getRaaUrls(baseUrl, html, keywords) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const links = doc.querySelectorAll('a');
    let urls = [];
    
    links.forEach(link => {
        const text = link.textContent.trim();
        keywords.forEach(keyword => {
            if (text.includes(keyword)) {
                const href = link.getAttribute('href');
                if (href && href.indexOf(".pdf") == -1) {
                    const url = new URL(href, baseUrl).href;
                    urls.push(url);
                }
            }
        });
    });
    
    return urls;
}

// Fonction pour extraire les liens PDF à partir de la page HTML
function getPdfs(html, lastUrl="") {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const links = doc.querySelectorAll('a[href$=".pdf"]');
    let pdfUrls = [];
    
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href != lastUrl) {
           pdfUrls.push(href);
        }
    });
    
    return pdfUrls;
}

// Fonction principale pour récupérer les RAA pour tous les départements
async function fetchAllRaa(annee) {
    const departements = [
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
    ];

    const results = [];
    for (const departement of departements) {
        const data = await fetchDepartementRaa(departement, annee);
        results.push({
            departement: departement,
            datas: data
        });
        await new Promise(resolve => setTimeout(resolve, 5000)); // Pause de 5 secondes
    }
    return results;
}

// Fonction pour récupérer les RAA pour un département donné
async function fetchPdfs(subPageUrl, lastUrl="") {
    const subPageContent = await getPage(subPageUrl);
    return getPdfs(subPageContent, lastUrl)
}

// Fonction pour récupérer les RAA pour un département donné
async function fetchDepartementRaa(departement, annee) {
    const baseUrl = `https://www.${departement}.gouv.fr`;
    const fullUrl = `${baseUrl}/Publications`;

    // STEP 1 : Détection de la page racine RAA
    let pageContent = await getPage(fullUrl);
    let raaUrls = getRaaUrls(baseUrl, pageContent, [
        "RAA", "actes administratifs", "Actes Administratifs", "Arrêtés préfectoraux"
    ]);

    // Workaround si on ne trouve pas l'url des RAA directement
    if (raaUrls.length === 0) {
        raaUrls = getRaaUrls(baseUrl, pageContent, [
            "Publications légales", "Publications administratives et légales"
        ]);
        if (raaUrls.length > 0) {
            pageContent = await getPage(raaUrls[0]);
            raaUrls = getRaaUrls(baseUrl, pageContent, [
                "RAA", "actes administratifs", "Actes Administratifs", "Arrêtés préfectoraux"
            ]);
        }
    }

    if (raaUrls.length === 0) {
        return {
            message: "Erreur, le programme ne peut pas analyser ce département",
            détails: "Veuillez analyser le site et ajouter le texte du lien dans les 'keywords'",
            url: fullUrl
        };
    }

    // STEP 2 : Détection des sous-pages années (ou paire années/mois)
    pageContent = await getPage(raaUrls[0]);
    const subPageUrls = getRaaUrls(baseUrl, pageContent, [
        `RAA ${annee}`, `Recueil des actes administratifs ${annee}`, `Année ${annee}`, `${annee}`
    ]);

    // STEP X : Récupération des liens de pdf
    const pdfs = [];
    for (const subPageUrl of subPageUrls) {
        const subPageContent = await getPage(subPageUrl);
        const monthUrls = getRaaUrls(baseUrl, subPageContent, [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]);

        if (monthUrls.length > 0) {
            for (const monthUrl of monthUrls) {
                const monthContent = await getPage(monthUrl);
                pdfs.push({
                    subpage_url: monthUrl,
                    pdfs: getPdfs(baseUrl, monthContent)
                });
            }
            return {
                publications: fullUrl,
                raa_url: raaUrls,
                subpage_urls: subPageUrls,
                links: pdfs
            };
        }

        pdfs.push({
            subpage_url: subPageUrl,
            pdfs: getPdfs(baseUrl, subPageContent)
        });
    }

    return {
        publications: fullUrl,
        raa_url: raaUrls,
        subpage_urls: subPageUrls,
        links: pdfs
    };
}

