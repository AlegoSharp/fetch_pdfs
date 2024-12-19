let selected_dpt;
let pdfLimit = 6;
const ANNEE = 2024;

function init_map() {
    let dpts = document.getElementsByClassName("departement");
    //let carte = document.getElementById("svgCarte");
        
    for (let index = 0; index < dpts.length; index++) {
        const element = dpts[index];
        element.setAttribute("fill", "#ffffff")
        element.addEventListener('click', selectDpt);
        //element.addEventListener('click', GetArretes);
        //let box = element.getBBox();
        //carte.appendChild(AddTextToSvg(box.x + (box.width/2), box.y + (box.height/2), element.getAttribute("data-numerodepartement")))
    }
}

async function addArrete(url) {
    if (!selected_dpt) {
        Swal.fire({
            title: 'Erreur',
            text: "Sélectionnez un département en cliquant dessus avant d'ajouter un arrêté !",
            icon: 'error',
            confirmButtonText: 'ok'
        });
    }
    let body = JSON.stringify({ 
        start: document.getElementById("dpt-new-raa-start").value,
        end: document.getElementById("dpt-new-raa-end").value,
        url: document.getElementById("dpt-new-raa").value,
    });
    const res = await fetch(`${window.origin}/api/${selected_dpt.slug}/addArrete`, {
        body: body,
        method: "POST",
        headers: new Headers({'content-type': 'application/json'}),
    })
    location.reload();
}

async function addUrl(url) {
    let added = false;
    let body = JSON.stringify({ 
        url: url,
    });

    await Swal.fire({
        title: "Voulez vous ajouter l'url à la base de données ?",
        text: url,
        icon: 'question',
        showDenyButton: true,
        confirmButtonText: 'Oui',
        denyButtonText: 'Non'
    }).then(async (result) => {
        if (result.isConfirmed) {
            const res = await fetch(`${window.origin}/api/${selected_dpt.slug}/addUrl`, {
                body: body,
                method: "POST",
                headers: new Headers({'content-type': 'application/json'}),
            })
            added = true;
        }
    });
    return added;
}

async function selectDpt(event){
    selected_dpt = event.target;
    if (selected_dpt) {
        document.getElementById("dpt-title").textContent = selected_dpt.dataset.nom + " ("+ selected_dpt.dataset.numerodepartement +")"
        document.getElementById("dpt_select").style.display = "block";
        
        const url = await fetch(`${window.origin}/api/${selected_dpt.dataset.numerodepartement}`, {
            headers: new Headers({'content-type': 'application/json'}),
        });
        const url_json = await url.json();

        selected_dpt.slug = url_json.departement_slug;
        selected_dpt.code = url_json.departement_code;

        // Display last url
        if (url_json.urls.length > 0) {
            document.getElementById("url-raa").href = url_json.urls[url_json.urls.length - 1].url;
            document.getElementById("url-raa").textContent = url_json.urls[url_json.urls.length - 1].url;
            selected_dpt.raa_url = url_json.urls[url_json.urls.length - 1].url;
            document.getElementById("div-search").style.display = "block";
            document.getElementById("search-url").style.display = "none";
        } else {
            document.getElementById("search-url").style.display = "block";
            document.getElementById("url-raa").href = "";
            document.getElementById("url-raa").textContent = "Ce département n'est pas sourcé.";
            document.getElementById("div-search").style.display = "none";
            selected_dpt.raa_url = "";
        }
        
        const arrete = await fetch(`${window.origin}/api/${selected_dpt.dataset.numerodepartement}/arretes`, {
            headers: new Headers({'content-type': 'application/json'}),
        });
        const arrete_json = await arrete.json();

        if (arrete_json.url != "") {
            document.getElementById("div-ongoing-arrete").style.display = "block";
            document.getElementById("current-arrete").href = arrete_json.url;
            document.getElementById("du").textContent = arrete_json.start;
            document.getElementById("au").textContent = arrete_json.end;
        } else {
            document.getElementById("div-ongoing-arrete").style.display = "none";
        }

    } else {
        document.getElementById("dpt_select").style.display = "none";
    }
}

async function showActions(){
    if (selected_dpt.raa_url === "") {
        await Swal.fire({
            title: 'Information',
            text: "Pas d'url enregistrée pour le département, recherche en cours ...",
            icon: 'info',
            confirmButtonText: 'ok'
        });
        await GetUrls();
        //await GetArretes();
    } else {
        await Swal.fire({
            title: 'Information',
            text: "Recherche des arrêtés en cours ...",
            icon: 'info',
            confirmButtonText: 'ok'
        });
        await GetArretes();
    }

    //Swal.fire({
    //	title: 'Quelle actions voulez vous effectuer ?',
    //	icon: 'question',
    //	showDenyButton: true,
    //	confirmButtonText: 'Chercher les urls',
    //	denyButtonText: 'Lire les PDF'
    //}).then(async (result) => {
    //	if (result.isConfirmed) {
    //		await GetUrls();
    //	} else if (result.isDenied) {
    //		await GetArretes();
    //	}
    //});
}

async function GetUrls() {
    const url = await fetch(`${window.origin}/api/${selected_dpt.dataset.numerodepartement}`, {
        headers: new Headers({'content-type': 'application/json'}),
    });
    
    const url_json = await url.json();
    let departement = url_json.departement_slug;
    
    let resp = await fetchDepartementRaa(departement, 2024);
    var table = document.getElementById("myTableUrls");
    console.log(resp);
    // insert data
    resp.raa_url.filter(onlyUnique).forEach(async function (item) {
        if(await addUrl(item)){
            var row = table.insertRow();
            addCell(row, item);
        }
    });
}

async function GetArretes() {
    let dataset = selected_dpt.dataset;
    const url = await fetch(`${window.origin}/api/${dataset.numerodepartement}`, {
        headers: new Headers({'content-type': 'application/json'}),
    });

    const url_json = await url.json();

    if (url_json.urls.length == 0) {
        Swal.fire({
            title: 'Erreur',
            text: "Impossible de trouver l'url des RAAs",
            icon: 'error',
            confirmButtonText: 'ok'
        });
        return;
    }
    
    for (let index = 0; index < url_json.urls.length; index++) {
        const element = url_json.urls[index];
        
        let resp_pdf = await fetchPdfs(element.url, element.lastUrl);
        
        if (document.getElementById("dpt-reverse").checked) {
            resp_pdf = resp_pdf.reverse();
        }
        if (document.getElementById("pdfLimit").value ) {
            pdfLimit = document.getElementById("pdfLimit").value;
        }

        for (let index = 0; index < resp_pdf.length; index++) {
            if (index >= pdfLimit) { break; }

            const pdf_url = resp_pdf[index];
            let body = JSON.stringify({ 
                url: pdf_url,
                dpt: dataset.numerodepartement
            });

            const response = await fetch(`${window.origin}/readPdf`, {
                body: body,
                method: "POST",
                headers: new Headers({'content-type': 'application/json'}),
            })
            let res = await response.json();
            if (res.match) {

                let start = new Date(res.start_date).toLocaleDateString()
                let end = new Date(res.end_date).toLocaleDateString()
                title = 'Arrêté préfectoral trouvé pour le departement : '
                title = title + dataset.nom + '(' + dataset.numerodepartement + ') '
                title = title + 'du ' + start + ' au ' + end
                await Swal.fire({
                    title: title,
                    text: res.pdf_url,
                    icon: 'warning',
                    confirmButtonText: 'ok'
                });
                var table = document.getElementById("myTableArretes");
                var row = table.insertRow();
                addCell(row, res.pdf_url);
            }
        }
    }
    await Swal.fire({
        title: 'Information',
        text: "La recherche des arrêté est terminée ...",
        icon: 'info',
        confirmButtonText: 'ok'
    });
}
