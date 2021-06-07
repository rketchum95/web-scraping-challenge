from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = "https://www.redplanetscience.com"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #scrape for the article title
    news_title = soup.find_all('div', class_="content_title").text

    #scrape for the article teaser paragraph
    news_para = soup.find_all('div', class_="article_teaser_body").text


    # Store data in a dictionary
    mars_news = {
        "article_title": news_title,
        "article_summary": news_para,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_news