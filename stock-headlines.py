import requests
from bs4 import BeautifulSoup
import openai
import os

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

# Set up the OpenAI API client
openai.api_key = "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"

# Combine all headlines
all_headlines = []
all_headlines.extend(get_yahoo_headlines())
all_headlines.extend(get_marketwatch_headlines())
all_headlines.extend(get_seeking_alpha_headlines())
all_headlines.extend(get_investing_headlines())
all_headlines.extend(get_cnbc_headlines())
all_headlines.extend(get_thestreet_headlines())

# Create the GPT-4 prompt
headlines_text = '\n'.join(all_headlines)
prompt = f"You are a financial advisor. You are going to receive many hundreds of headlines from financial news websites, and I want you to use that information to produce me a list of 10 stocks you think are going to perform relatively well tomorrow, as a result of all this news. That is, if you think the stock will see a +2% or higher return, go ahead and list it. If you can't think of any such stocks, or you can only think of fewer than 10, that's fine. Just give as many as you can, up to 10. If possible, provide the reasoning for each.\n\nHere are the headlines:\n{headlines_text}\n\nBased on these headlines, the stocks to consider are:"

# Query GPT-4
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a financial advisor. You are going to receive many hundreds of headlines from financial news websites, and I want you to use that information to produce me a list of 10 stocks you think are going to perform relatively well tomorrow, as a result of all this news. That is, if you think the stock will see a +2% or higher return, go ahead and list it. If you can't think of any such stocks, or you can only think of fewer than 10, that's fine. Just give as many as you can, up to 10. If possible, provide the reasoning for each."
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