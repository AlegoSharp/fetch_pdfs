from flask import Flask, jsonify, request
from Fetcher import Fetcher
from Scraper import Scraper
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
fetcher = Fetcher()

@app.route('/api/<departement>', methods=['GET'])
def get_data(departement):
    base_url = f'https://www.{departement}.gouv.fr'
    full_url = f'{base_url}/Publications'
    raa_url = ""

    keywords = [
        "RAA",  
        "actes administratifs"
    ]

    res = fetcher.get_page(full_url,"get")
    scraper = Scraper(res.content)
    raa_url = scraper.get_raa_url(keywords)

    return jsonify({
        'url': f'{base_url}{raa_url}',
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)