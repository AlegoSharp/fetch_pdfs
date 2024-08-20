from sqlalchemy import Column, Integer, String, Text, ForeignKey

from sqlalchemy.orm import relationship

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