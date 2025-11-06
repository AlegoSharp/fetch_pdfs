from flask import Flask, jsonify, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import urllib.request
import ssl

import Engine
import DbModels
import PdfReader
import datetime
from datetime import date

app = Flask(__name__)
app.json.sort_keys = False

# Configuration de la base de données
DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Session pour interagir avec la base de données
Session = sessionmaker(bind=engine)


@app.route('/', methods=['GET'])
def mapSearch():
   session = Session()
   arretes = []
   raa_urls = []
   urls = session.query(DbModels.Raa).all()
   now = datetime.datetime.now().strftime('%Y-%m-%d')
   pdf_link= session.query(DbModels.PdfLink).where(DbModels.PdfLink.end_date>=now).all()
   for link in pdf_link:
      dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_id == link.departement_id).first()
      arretes.append({
         "code": dpt.departement_code,
         "url": f"https://{dpt.departement_slug}.gouv.fr{link.pdf_url}"
      })
   for url in urls:
      dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_id == url.departement_id).first()
      raa_urls.append({
         "code": dpt.departement_code,
         "url": url.raa_url
      })
   session.close()
   return render_template("map.html", arretes=arretes, raa_urls=raa_urls, urls=urls) 

@app.route('/config', methods=['GET'])
def config():
   return render_template("config.html") 

@app.route('/api/config', methods=['GET'])
def getConfig():
   session = Session()
   dpt_raa_urls = []

   dpts = session.query(DbModels.Departement).all()
   for dpt in dpts:
      url = session.query(DbModels.Raa).where(DbModels.Raa.departement_id == dpt.departement_id).first()
      if url:
         dpt_raa_urls.append({
            "dpt": dpt.departement_code,
            "slug": dpt.departement_slug,
            "url": url.raa_url
         })
      else:
         dpt_raa_urls.append({
            "dpt": dpt.departement_code,
            "slug": dpt.departement_slug,
            "url": ""
         })

   session.close()

   return jsonify(dpt_raa_urls)
 

@app.route('/api/<dpt_code>', methods=['GET'])
def fetch_urls(dpt_code):
   session = Session()
   res = []

   dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_code == dpt_code).first()
   urls = session.query(DbModels.Raa).where(DbModels.Raa.departement_id == dpt.departement_id).all()

   res = {
      "departement_code": dpt.departement_code,
      "departement_slug": dpt.departement_slug,
      "urls": []
   }
   for url in urls:
      res['urls'].append({
         "url": url.raa_url,
         "lastUrl": url.publications_url
      })

   session.close()
   return jsonify(res)


@app.route('/api/<slug>/addUrl', methods=['POST'])
def add_url(slug):
   session = Session()
   session.expire_on_commit = False
   dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_slug == slug).first()

   datas = request.get_json()

   new_raa = DbModels.Raa(
      departement_id= dpt.departement_id,
      year = 2025,
      raa_url = datas["url"],
   )

   session.add(new_raa)
   session.commit()

   session.close()

   return jsonify({
      "departement_id": dpt.departement_id,
      "year": 2025,
      "raa_url": datas["url"],
   })

@app.route('/api/<slug>/addArrete', methods=['POST'])
def add_arrete(slug):
   session = Session()
   session.expire_on_commit = False
   dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_slug == slug).first()

   datas = request.get_json()

   new_raa = DbModels.PdfLink(
      departement_id= dpt.departement_id,
      start_date = datas['start'],
      end_date = datas['end'],
      pdf_url = datas['url'],
   )

   session.add(new_raa)
   session.commit()

   session.close()

   return jsonify({
      "departement_id": dpt.departement_id,
      "year": 2025,
      "raa_url": datas["url"],
   })

@app.route('/readPdf', methods=['POST'])
def readPdf():
   session = Session()

   datas = request.get_json()
   dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_code == datas['dpt']).first()
   
   pdfsResults = PdfReader.readPdf(dpt, datas['url'])

   #if pdfsResults['match']:
   #   #if pdfsResults['start_date'] == "" or pdfsResults['end_date'] == "":
   #   #   return jsonify({
   #   #      "error": "La date du RAA n'a pas été trouvée",
   #   #      "fichier": f"https://{dpt.departement_slug}.gouv.fr{datas['url']}"
   #   #   })
      #new_pdf = DbModels.PdfLink(
      #   departement_id=dpt.departement_id,
      #   start_date=pdfsResults['start_date'],
      #   end_date=pdfsResults['end_date'],
      #   pdf_url=datas['url']
      #)
      #session.add(new_pdf)
      #session.commit()
   
   session.close()
   return jsonify(pdfsResults)

@app.route('/api/<departement>/<annee>/pdfs', methods=['GET'])
def fetch_departement(departement, annee):
   return jsonify(Engine.fetch_departement_raa(departement,annee))


@app.route('/api/<annee>/pdfs', methods=['GET'])
def fetch_all(annee):
   return jsonify(Engine.fetch_all_raa(annee))

@app.route('/api/<departement>/arretes', methods=['GET'])
def fetch_arretes(departement):
   session = Session()
   dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_code == departement).first()
   arrete = session.query(DbModels.PdfLink).where(DbModels.PdfLink.departement_id == dpt.departement_id).where(DbModels.PdfLink.end_date >= date.today()).order_by(DbModels.PdfLink.end_date.desc()).first()
   url = ""
   start = {}
   end = {}
   if arrete:
      url = arrete.pdf_url
      start = arrete.start_date.strftime('%d.%m.%y')
      end = arrete.end_date.strftime('%d.%m.%y')

   res = {
      "departement_code": dpt.departement_code,
      "departement_slug": dpt.departement_slug,
      "url": url,
      "start": start,
      "end": end
   }

   return jsonify(res)

@app.route('/api/<departement>/attrap', methods=['GET'])
def fetch_attrap(departement):
   data = {}
   context = ssl._create_unverified_context()
   session = Session()
   dpt = session.query(DbModels.Departement).where(DbModels.Departement.departement_code == departement).first()
   
   administration = "pref"+dpt.departement_code
   url = "https://attrap.fr/api/v1/search?s=%22rave%22&sort=desc&administration="+administration

   with urllib.request.urlopen(url, context=context) as res:
         data = res.read()

   return data



@app.route('/api/fb/<page>', methods=['GET'])
def fb_fetch(page):
   return jsonify(page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)