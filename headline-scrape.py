import requests
from bs4 import BeautifulSoup
import sys

if len(sys.argv) < 2:
    print("Please provide a stock ticker symbol as a command line argument.")
    sys.exit(1)

ticker = sys.argv[1]
url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

headlines = soup.find_all('h3', class_='Mb(5px)')

for headline in headlines:
    print(headline.text)