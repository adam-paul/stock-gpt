import requests
from bs4 import BeautifulSoup
import openai
import os
import concurrent.futures

def get_yahoo_headlines():
    url = 'https://finance.yahoo.com/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('h3', class_='Mb(5px)', limit=100)
    headline_list = [headline.text for headline in headlines]
    
    return headline_list

def get_marketwatch_headlines():
    url = 'https://www.marketwatch.com/latest-news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('h3', class_='article__headline', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_seeking_alpha_headlines():
    url = 'https://seekingalpha.com/market-news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('div', class_='media-body', limit=100)
    headline_list = [headline.a.text.strip() for headline in headlines]

    return headline_list

def get_investing_headlines():
    url = 'https://www.investing.com/news/latest-news'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('article', class_='js-article-item', limit=100)
    headline_list = [headline.find('a', class_='title').text.strip() for headline in headlines]

    return headline_list

def get_cnbc_headlines():
    url = 'https://www.cnbc.com/latest-news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('div', class_='Card-titleText', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]
    
    return headline_list

def get_thestreet_headlines():
    url = 'https://www.thestreet.com/latest-news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('h2', class_='text__headline', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_zacks_headlines():
    url = 'https://www.zacks.com/stock/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('a', class_='article_title', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_benzinga_headlines():
    url = 'https://www.benzinga.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('h3', class_='it-teaser__title', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_reuters_headlines():
    url = 'https://www.reuters.com/finance'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('h3', class_='story-title', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_business_insider_headlines():
    url = 'https://www.businessinsider.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('h2', class_='tout__title', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_ft_headlines():
    url = 'https://www.ft.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('a', class_='js-teaser-heading-link', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

def get_economist_headlines():
    url = 'https://www.economist.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    headlines = soup.find_all('span', class_='teaser__headline', limit=100)
    headline_list = [headline.text.strip() for headline in headlines]

    return headline_list

# Set up the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

# A list of your scraping functions
scraping_functions = [get_yahoo_headlines, get_marketwatch_headlines, get_seeking_alpha_headlines, 
                      get_investing_headlines, get_cnbc_headlines, get_thestreet_headlines, 
                      get_zacks_headlines, get_benzinga_headlines]

# Use a ThreadPoolExecutor to run the functions concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(lambda f: f(), scraping_functions)

# Combine all headlines
all_headlines = []
for result in results:
    all_headlines.extend(result)

# Create the GPT-4 prompt
headlines_text = '\n'.join(all_headlines)

# Query GPT-4
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a financial advisor. You are going to receive many headlines from financial news websites, and I want you to use that information to produce  a list of stocks you think are going to perform  well tomorrow. If you think the stock will see a positive return, name the stock, give your probability it's going to go up tomorrow (and by how much), and provide a sentence for why. If you think a stock will go down or if you are uncertain about a stock, don't bother listing it.\n\nHere are the headlines:"
        },
        {
            "role": "user",
            "content": headlines_text
        }
    ],
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.7,
)

# Save the response to a .txt file
with open("gpt_response.txt", "w") as file:
    file.write(response['choices'][0]['message']['content'].strip())

print("GPT-4 response saved to gpt_response.txt")