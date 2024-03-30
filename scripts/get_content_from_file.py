from bs4 import BeautifulSoup
import requests


response = requests.get('https://tailwindcss.com/docs/customizing-colors')

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.find(id="content-wrapper").text)