from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base pour la déclaration des modèles
Base = declarative_base()

class Departement(Base):
    __tablename__ = 'departement'
    
    departement_id = Column(Integer, primary_key=True)
    departement_code = Column(String(10), nullable=False)
    departement_nom = Column(String(255), nullable=False)
    departement_nom_uppercase = Column(String(255), nullable=False)
    departement_slug = Column(String(255), nullable=False)
    departement_nom_soundex = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Departement(departement_id={self.departement_id}, departement_nom='{self.departement_nom}')>"

class Raa(Base):
    __tablename__ = 'raa'

    id = Column(Integer, primary_key=True)
    departement_id = Column(Integer, ForeignKey('departement.departement_id'))
    year = Column(String(4), nullable=False)
    publications_url = Column(Text)
    raa_url = Column(Text)

class PdfLink(Base):
    __tablename__ = 'pdf_link'

    id = Column(Integer, primary_key=True)
    departement_id = Column(Integer, ForeignKey('departement.departement_id'))
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    pdf_url = Column(Text, nullable=False)
