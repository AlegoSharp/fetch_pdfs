import requests
from bs4 import BeautifulSoup
# Replace this with the URL for the desired year
url = 'https://www.finistere.gouv.fr/Publications/Recueil-des-actes-administratifs/Recueils-publies-en-2024/'
headers = {'User-Agent': 'whatever'}
# Send an HTTP request to the URL
response = requests.get(url, headers=headers)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the links to the PDF files
pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

# Print the PDF links
for link in pdf_links:
    print(f'https://www.finistere.gouv.fr{link}')
