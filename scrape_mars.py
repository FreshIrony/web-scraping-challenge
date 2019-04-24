#!/usr/bin/env python
# coding: utf-8

# In[6]:


from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd

def scrape():
    # In[7]:


    # Setup ChromeDriver environment
    executable_path = {'executable_path':'C:/Users/Anthony Stansall/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)


    # In[8]:


    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")

    # Assign the text to variables that you can reference later.
    time.sleep(2)
    news_title = soup.find('div', class_="bottom_gradient").text
    time.sleep(2)
    news_p = soup.find('div', class_="rollover_description_inner").text


    # In[9]:


    # Visit the url for JPL Featured Space Image 
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")

    # Assign the url string to a variable called featured_image_url
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path
    # print(featured_image_url)


    # In[10]:


    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')

    # Save the tweet text for the weather report as a variable called mars_weather.
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # print(mars_weather)


    # In[11]:


    # Visit the Mars Facts webpage
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')
    mars_data = soup.find('table', class_="tablepress tablepress-id-mars")


    # In[12]:


    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    table = mars_data.find_all('tr')

    labels = []
    values = []

    for tr in table:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
        
    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })

    # Use Pandas to convert the data to a HTML table string.
    mars_facts = mars_facts_df.to_html(header = False, index = False)
    # mars_facts


    # In[21]:


    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_html = browser.html
    soup = BeautifulSoup(usgs_html, "html.parser")
    hemisphere_links = soup.find_all('div', class_='description')


    # In[47]:


    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys img_url and title.
    hemisphere_image_urls = []
    for x in hemisphere_links:
        title = x.find('h3').text
        image_links = "https://astrogeology.usgs.gov/" + x.find('a')['href']
        soup = BeautifulSoup((requests.get(image_links)).text, 'lxml')
        download = soup.find('div', class_='downloads')
        img_url = download.find('a')['href']
        hemisphere_image_urls.append({"Title": title, "Image_Url": img_url})
    # print(hemisphere_image_urls)

    full_mars_data = {
        "Title": news_title,
        "Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Facts": mars_facts,
        "Hemisphere_Images": hemisphere_image_urls
        }

    return full_mars_data