import requests 
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 
    'Accept-Language': 'en-US, en;q=0.5'
}

search_query = 'winter jacket'.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

items = []
for i in range(1,11):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url+'&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    print(base_url + '&page={0}'.format(i))
    
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results: 
        product_name = result.h2.text
        try: 
            rating = result.find('i', {'class':'a-icon'}).text 
            rating_count = result.find('span', {'class': 'a-size-base'}).text
        except AttributeError:
            continue 
        try: 
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float(price1 + '.' + price2)
        except AttributeError:
            price = None  # If price not found, set to None

        product_url_tag = result.h2.a
        if product_url_tag:  # Check if the 'a' tag exists
            product_url = 'https://amazon.com' + product_url_tag['href']
        else:
            product_url = None  # If the 'a' tag is not found, set the URL to None

        items.append([product_name, rating, rating_count, price, product_url])

    # Make sure to adjust the DataFrame creation to include product_url
    df = pd.DataFrame(items, columns=['product', 'ratings', 'rating_count', 'price', 'product_url'])
    df.to_csv('{0}.csv'.format(search_query), index=False)
