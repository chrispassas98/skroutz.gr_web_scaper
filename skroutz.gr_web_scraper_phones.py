#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# URL of the site to scrape
base_url = 'https://www.skroutz.gr/c/40/kinhta-thlefwna.html'

# Making a list to store the phones
phones = []

# Loop through the pages, so we can scrape them all
for page_num in range(1, 56):
    # Construct the URL for the current page
    url = f'{base_url}?page={page_num}'
    
    # Generate random agents so the site won't block us.
    headers = {
        "User-Agent": UserAgent().random
    }

    print(f"Processing page {page_num}")
    
    # URL request, if failed we can see which page failed. If we scrape the page successfully we continue.
    try:
        req = Request(url, headers=headers)
        response = urlopen(req)
        page = response.read()
    except HTTPError as e:
        print(f"HTTP error occurred for page {page_num}: {e.code}")
        continue
    except URLError as e:
        print(f"URL error occurred for page {page_num}: {e.reason}")
        continue
    
    # Beautiful Soup to scrape our data
    soup = BeautifulSoup(page, 'html.parser')
    
    # Finding all listings
    listings = soup.find_all('li', class_='cf card')
    
    # Loop through each listing and extract the desired information
    for listing in listings:
        phone = {}  # Making a dictionary to store our info

        # Extract title
        title = listing.find('a', class_="js-sku-link")
        phone['Title'] = title['title'].strip() if title else 'N/A'
        
        # Extract price
        price_tag = listing.find('a', class_='js-sku-link sku-link')
        if price_tag:
            price_text = price_tag.text.replace('από', '').strip()
            phone['Price'] = price_text
        else:
            phone['Price'] = 'N/A'

        # Extract key features
        specs = listing.find('p', class_='specs')
        if specs:
            title_attr = specs.get('title', '')
            details = title_attr.split(', ')
            for detail in details:
                if "Μοντέλο" in detail:
                    phone['Model'] = detail.split(': ')[1]
                elif "Οθόνη" in detail:
                    phone['Screen'] = detail.split(': ')[1]
                elif "Μπαταρία" in detail:
                    phone['Battery'] = detail.split(': ')[1]

        # Extract rating
        rating = listing.find('div', class_='actual-rating')
        phone['Rating'] = rating.text.strip() if rating else 'N/A'

        # Extract number of reviews
        reviews = listing.find('div', class_='reviews-count')
        phone['Reviews'] = reviews.text.strip() if reviews else 'N/A'
        
        # Extract reviews in stars from 1 to 5
        reviews2 = listing.find('a', class_ ="rating stars")
        phone['Stars_Reviews'] = reviews2['title'].strip() if reviews2 else 'N/A'
    
        # Extract shops that have the phone available to order
        stock = listing.find('span', class_ = "shop-count")
        phone['Shop_Stock'] = stock.text.strip() if stock else 'N/A'
        
        # Append the phone details to the phones list
        phones.append(phone)
    # Print results to see if our code works
    print(f"Completed processing page {page_num}")
    print(f"Total phones scraped so far: {len(phones)}")

    # adding delay
    time.sleep(10)

print("Scraping complete")

# Print the extracted data
for phone in phones:
    print(phone)


# In[4]:


# adding our data to a DataFrame

df = pd.DataFrame(phones)
df


# In[5]:


df.astype


# In[ ]:




