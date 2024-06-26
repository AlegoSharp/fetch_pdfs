import os
import re
import random
import ssl
import subprocess
import shutil
import string
import logging
import requests
import time
import datetime
import json
from urllib.parse import quote

import dateparser

from bs4 import BeautifulSoup

logger = logging.getLogger("yo")

class Fetcher:
    def __init__(self):
        self.session = requests.Session()
        self.tor_max_requests = 0
        self.tor_requests = 0
        self.tor_socks5_key = None
        self.sleep_time = 1


    def tor_get_new_id(self):
        """Change de circuit Tor. Cela permet de changer de noeud de sortie donc d'IP."""
        self.tor_socks5_key = 'attrap_' + ''.join(random.choices(string.ascii_lowercase, k=20))
        proxies = {
            "http": f"socks5h://attrap:{self.tor_socks5_key}@127.0.0.1:9050",
            "https": f"socks5h://attrap:{self.tor_socks5_key}@127.0.0.1:9050",
        }
        self.session.proxies.update(proxies)
        self.tor_requests = 0
        
    def get_page(self, url, method, data={}):
        """
        Récupère le contenu HTML d'une page web

        url -- L'URL de la page demandée
        method -- 'post' ou 'get', selon le type de requête
        data -- Un dictionnaire contenant les données à envoyer au site
        """
        try:
            logger.debug(f'Chargement de la page {url}')
            if self.sleep_time > 0:
                time.sleep(self.sleep_time)

            self.session.headers.update({'User-Agent': "whatever"})

            page = None
            if method == 'get':
                page = self.session.get(url, timeout=(10, 120))
            if method == 'post':
                page = self.session.post(url, data=data, timeout=(10, 120))

            if page.status_code == 429:
                logger.warning('Erreur 429 Too Many Requests reçue, temporisation...')
                self.tor_get_new_id()
                time.sleep(1)
                return self.get_page(url, method, data)

            self.tor_requests += 1
            if self.tor_max_requests > 0 and \
                self.tor_requests > self.tor_max_requests:
                self.tor_get_new_id()

            return page
        except requests.exceptions.ConnectionError:
            logger.warning(f'Erreur de connexion, temporisation...')
            self.tor_get_new_id()
            time.sleep(30)
            return self.get_page(url, method, data)
        except requests.exceptions.Timeout:
            logger.warning(f'Timeout, on relance la requête...')
            return self.get_page(url, method, data)