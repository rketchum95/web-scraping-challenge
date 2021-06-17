# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():
#
    #Chrome driver set up
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_info = {}

#def scrape_info():
    #Visit NASA site
    url = 'https://www.redplanetscience.com'
    browser.visit(url)

    html = browser.html
    soup = bs(html,'html.parser')
    result = soup.find('div', class_='list_text')

    # Identify and return title of listing
    article_title = result.find('div', class_='content_title').text
    # Identify and return article summary
    article_summary = result.find('div', class_='article_teaser_body').text

    mars_info['title'] = article_title
    mars_info['summary'] =  article_summary


    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    html1 = browser.html
    soup = bs(html1,'html.parser')

    # Locate featured image
    results = soup.find('div', class_='floating_text_area')
    featured_image_url = results.find('a')['href']

    # Concatinate for complete URL
    featured_image_url1 = jpl_url + featured_image_url

    mars_info['feature_image'] = featured_image_url1

    # mars fact table
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_facts_url)

    html2 = browser.html
    soup = bs(html2,'html.parser')

    #read table from mars facts url
    tables = pd.read_html(mars_facts_url)
    tables[0]

    #create dataframe from table
    mars_facts = tables[0]

    #Clean up df
    mars_facts.columns =mars_facts.iloc[0]
    mars_facts_df = mars_facts[1:]
    mars_facts_df.set_index('Mars - Earth Comparison', inplace=True)
    mars_facts_df

    # Save dataframe as html file
    html_table = mars_facts_df.to_html(justify="left", classes="table table-striped")

    mars_info['mars_facts'] = html_table

    # Mars hemisphere info
    mars_hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemisphere_url)

    html = browser.html
    soup = bs(html,'html.parser')

    # Scrape site for needed info
    results = soup.find_all('div', class_='item')

    # Create empty list to store data 
    hemisphere_image_urls = []

    # Loop through returned results
    for result in results:  
        
        # Identify and return title 
        hemisphere_title = result.find('h3').text
        hemisphere_page = result.find('a', class_='itemLink product-item')['href']
        hemisphere_img_url = mars_hemisphere_url + hemisphere_page
        
        # scrape img_url to get full size image url
        browser.visit(hemisphere_img_url)
        html = browser.html
        soup = bs(html,'html.parser')
        full_hem_img = soup.find_all('a', href=True)[3]['href']
        
        #Concatinate for final dictionary
        full_hem_img1 = mars_hemisphere_url + full_hem_img
        
        # create document for dictionary
        #url = {"title": hemisphere_title, "img_url": full_hem_img1}

        #append dictionary
        hemisphere_image_urls.append({"title": hemisphere_title, "img_url": full_hem_img1})
        
    mars_info['hemisphere_info'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()
        
    # mars_data = {mars_news, feature_image, mars_facts, hemisphere_image_urls}
    #              "article_summary": article_summary, 
    #              "featured_image_url1": featured_image_url1, 
    #              "html_table": html_table, 
    #              "hemi_image_url": hemisphere_image_urls}
    return mars_info
# collection.insert(mars_data)



