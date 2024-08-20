-- Table pour les départements
CREATE TABLE departement (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table pour les RAA
CREATE TABLE raa (
    id SERIAL PRIMARY KEY,
    departement_id INT REFERENCES departement(id),
    year VARCHAR(4) NOT NULL,
    publications_url TEXT,
    raa_url TEXT
);

-- Table pour les sous-pages
CREATE TABLE subpage (
    id SERIAL PRIMARY KEY,
    raa_id INT REFERENCES raa(id),
    subpage_url TEXT NOT NULL
);

-- Table pour les liens PDF
CREATE TABLE pdf_link (
    id SERIAL PRIMARY KEY,
    subpage_id INT REFERENCES subpage(id),
    pdf_url TEXT NOT NULL
);
