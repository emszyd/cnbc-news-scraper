import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_news():
    url = 'https://www.cnbc.com/politics/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    #loop through all article containers
    for article in soup.find_all('div', class_='Card-titleAndFooter'):
        #find the headline element and extract the text
        headline_element = article.find('a', class_='Card-title')
        headline = headline_element.text.strip()
        
        #extract the link from the 'href' attribute
        link = headline_element['href']

        #check if the link is a full url or relative path
        article_url = link if link.startswith('http') else f"{url}{link}"
        
        #print to debug
        print(f"Article URL: {article_url}")

        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        #find the content and extract the text
        content_element = article_soup.find('div', class_ = 'ArticleBody-articleBody')
        content = content_element.text.strip() if content_element else "Content not found"

        articles.append({'headline': headline, 'content': content, 'url': article_url})

    return pd.DataFrame(articles)


if __name__ == '__main__':
    df = scrape_news()
    df.to_csv('scraped_news.csv', index=False)