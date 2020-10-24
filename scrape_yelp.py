# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

# Inittizalize splinter function
def initiate_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = initiate_browser()
    
    # Putting reviews into a list
    yelp_reviews = []

    # start from the first page on yelp and go to the fifth page
    start = 0
    num_pages = 5
    end = 20* num_pages

    # loop through yelp page to scrape the comments

    while (start < end):
        yelpurl = 'https://www.yelp.com/biz/9292-korean-bbq-duluth-3?osq=9292'
        url = yelpurl + '&start=' + str(start)
        start += 20
        browser.visit(url)
        yelphtml = browser.html
        yelpsoup = BeautifulSoup(yelphtml, 'html.parser')

        allcomment = yelpsoup.find_all('p', class_='lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-')

        for x in range(0,len(allcomment)):    
            yelp_reviews.append(allcomment[x].text)

    # Close the browser
    browser.quit()

    yelp_information = {"Yelp_Reviews": yelp_reviews}

    return yelp_information



