from bs4 import BeautifulSoup
import re

class Scraper:
    def __init__(self, url, content):
        self.soup = BeautifulSoup(content, 'html.parser')
        self.url = url

    def get_sub_pages(self, keywords):
        return None

    def get_raa_urls(self, keywords, breakOnKeywords = True):
        raa_urls=[]

        # Removing all nav tag to avoid parsing wrong links
        for nav in self.soup.find_all('nav'):
            nav.decompose()
        
        # Parse the HTML content of the page
        for keyword in keywords:
            links = self.soup.find_all("a", href=re.compile("/Publications/"), string=re.compile(keyword))
            for link in links:                    
                if link['href'] is not None and f"{self.url}{link['href']}" not in raa_urls:
                    raa_urls.append(f"{self.url}{link['href']}")

            if len(raa_urls) > 0 and breakOnKeywords:
                break
        return raa_urls

    def get_pdfs(self):
        links = []
        for link in self.soup.find_all('a'):
            current_link = link.get('href')
            if current_link is not None and current_link.endswith('pdf'):
                links.append(f'{self.url}{current_link}')
    
        return links