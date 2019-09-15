# Import dependencies
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import requests
#from selenium import webdriver
#driver = webdriver.Chrome()
from splinter import Browser

# scraping fundtion
def scrape():
    mars_data = {}

    # Get web info from mars news sight
    # Comment: using "request.get" was not providing the latest website, i switched to "Broswer" option!
    # The jupyter notebook contains the code for both options (comment applies!).
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_="image_and_description_container")
    news_title = results[0].find_all("h3")[0].text
    news_p = results[0].a.div.div.text.strip('\n')
    browser.quit()

    # Use splinter to get image from NASA page
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Sometimes visit to partial link gives error in featured image, hence the while / try statement
    while True:
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)
        time.sleep(1)
        browser.click_link_by_partial_text('FULL')
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        results = soup.find_all('div',class_="fancybox-inner")
    
        try:
            featured_image_url = "https://www.jpl.nasa.gov" + results[0].find_all("img")[0]["src"]
            break
        except:
            cont = True

    browser.quit()

    # Pull Weather Data from Twitter
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    results = soup.find_all("p",class_="TweetTextSize")
    for result in results:
        if (result.text[0:7] == "InSight"):
            mars_weather = result.text
            break

    # Mars Facts
    url = "https://space-facts.com/mars/"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    tables = pd.read_html(url)
    df_mars = tables[0]
    df_mars = df_mars.drop("Earth",1)
    df_mars.columns = ["Parameter", "Value"]
    df_mars = df_mars.set_index("Parameter")
    df_mars.to_html('Mars_Parameters.html')
    mars_html = df_mars.to_html()
    mars_html = mars_html.replace("\n", "")

    #Get Hemisphere data
    labels = ["Valles", "Cerberus", "Schiaparelli", "Syrtis"]
    hemisphere_image_urls = []

    for label in labels:
        # Setup splinter drivers
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)

        # Go to spcae images
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        time.sleep(1)
        browser.click_link_by_partial_text(label)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        soup.find("h2",class_="title").text
        results = soup.find_all('div',class_="downloads")
        hemisphere_image_urls.append({"title": soup.find("h2",class_="title").text, "img_ulr" : results[0].li.a["href"]})
        browser.quit()

    # Store resutls of web scrapping
    mars_data = {"news_title" : news_title,
                "news" : news_p,
                "featured" : featured_image_url,
                "weather" : mars_weather,
                "mars_data": mars_html,
                "hemisphere" : hemisphere_image_urls
                }
    
    return mars_data

#print(scrape())
