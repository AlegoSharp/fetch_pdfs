from bs4 import BeautifulSoup
import re

class Scraper:
    def __init__(self, content):
        self.soup = BeautifulSoup(content, 'html.parser')

    def get_raa_url(self, keywords):
        # Parse the HTML content of the page
        for keyword in keywords:
            tag = self.soup.find('a', string=re.compile(keyword))

            if tag is not None:
                if tag['href'] is not None and tag['href'] != "":
                    raa_url = tag['href']
                    break
        return raa_url
