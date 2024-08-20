import io
from flask import Flask, render_template, request, redirect, url_for
import requests 
import Engine
import PyPDF2
import re

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
app.json.sort_keys = False

def read_pdf():
    # open the pdf file
    reader = PyPDF2.PdfReader("test.pdf")

    # define key terms
    string = "festif"

    # extract text and do the search
    for page in reader.pages:
        text = page.extract_text() 
        # print(text)
        res_search = re.search(string, text)
    return res_search


app.jinja_env.globals.update(read_pdf=read_pdf)
# Configuration de la base de données
DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base pour la déclaration des modèles
Base = declarative_base()

# Session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()

class Departement(Base):
    __tablename__ = 'departement'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    raas = relationship("Raa", back_populates="departement")

class Raa(Base):
    __tablename__ = 'raa'

    id = Column(Integer, primary_key=True)
    departement_id = Column(Integer, ForeignKey('departement.id'))
    year = Column(String(4), nullable=False)
    publications_url = Column(Text)
    raa_url = Column(Text)
    subpages = relationship("Subpage", back_populates="raa")
    departement = relationship("Departement", back_populates="raas")

class Subpage(Base):
    __tablename__ = 'subpage'

    id = Column(Integer, primary_key=True)
    raa_id = Column(Integer, ForeignKey('raa.id'))
    subpage_url = Column(Text, nullable=False)
    pdf_links = relationship("PdfLink", back_populates="subpage")
    raa = relationship("Raa", back_populates="subpages")

class PdfLink(Base):
    __tablename__ = 'pdf_link'

    id = Column(Integer, primary_key=True)
    subpage_id = Column(Integer, ForeignKey('subpage.id'))
    pdf_url = Column(Text, nullable=False)
    subpage = relationship("Subpage", back_populates="pdf_links")


@app.route('/map', methods=['GET'])
def map():
   urls = session.query(Raa).all()
   arretes = ['29', '01', '07', '41'] 
   return render_template("map.html", arretes=arretes, urls=urls) 

@app.route('/readPdf', methods=['POST'])
def readPdf():
    data = request.get_json()
    headers = {"User-Agent": "yyyy"}
    response = requests.get(data['url'], headers=headers)

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

@app.route('/api/<departement>/<annee>/pdfs', methods=['GET'])
def fetch_departement(departement, annee):
   return jsonify(Engine.fetch_departement_raa(departement,annee))

@app.route('/api/<annee>/pdfs', methods=['GET'])
def fetch_all(annee):
   return jsonify(Engine.fetch_all_raa(annee))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)