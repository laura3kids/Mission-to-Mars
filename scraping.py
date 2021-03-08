# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

driver = webdriver.Chrome(ChromeDriverManager().install())

# Windows users
executable_path = {'executable_path':
                   "C:\\Users\\laura\\.wdm\\drivers\\chromedriver\\win32\\88.0.4324.96\\chromedriver.exe"}

def scrape_all():
    # Initiate headless driver for deployment                   
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Scrape the Title
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')
        
    except AttributeError: 
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException: 
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

    # Convert dataframe back to html
    return df.to_html()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

def hemisphere_data():
    # Scrape astrogeology.usgs.gov for hemisphere image urls and titles
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = soup(hemisphere_html, 'html.parser')
    base_url ="https://astrogeology.usgs.gov"

    image_list = hemisphere_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for image in image_list:
        #initialize a dictionary
        hemisphere_dict = {}
        
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        hemisphere_html2 = browser.html
        hemisphere_soup2 = soup(hemisphere_html2, 'html.parser')
        
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
        
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
        
        # Append dictionary to list
        hemisphere_image_urls.append(hemisphere_dict)
        mars_results["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_results

