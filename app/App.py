from flask import Flask, jsonify, render_template, request

import PyPDF2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import Engine
import DbModels
import PdfReader

app = Flask(__name__)
app.json.sort_keys = False

# Configuration de la base de données
DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base pour la déclaration des modèles
Base = declarative_base()

# Session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/map', methods=['GET'])
def map():
   urls = session.query(DbModels.Raa).all()
   arretes = ['29', '01', '07', '41'] 
   return render_template("map.html", arretes=arretes, urls=urls) 

@app.route('/readPdf', methods=['POST'])
def readPdf():
    PdfReader.readPdf(request.get_json())

@app.route('/api/<departement>/<annee>/pdfs', methods=['GET'])
def fetch_departement(departement, annee):
   return jsonify(Engine.fetch_departement_raa(departement,annee))

@app.route('/api/<annee>/pdfs', methods=['GET'])
def fetch_all(annee):
   return jsonify(Engine.fetch_all_raa(annee))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)