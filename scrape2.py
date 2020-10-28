from flask import Flask, render_template, jsonify, request
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

#Creating functions to webscrape
# Inittizalize splinter function
def initiate_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape(yelpurl):
    browser = initiate_browser()
    
    # Putting reviews into a list
    yelp_reviews = []
    yelp_stars = []

    # start from the first page on yelp and go to the fifth page
    start = 0
    num_pages = 1
    end = 20* num_pages

    # loop through yelp page to scrape the comments

    while (start < end):
        url = yelpurl + '&start=' + str(start)
        start += 20
        browser.visit(url)
        yelphtml = browser.html
        yelpsoup = BeautifulSoup(yelphtml, 'html.parser')

        allcomment = yelpsoup.find_all('p', class_='lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-')

        for x in range(0,len(allcomment)):    
            yelp_reviews.append(allcomment[x].text)

        # Finding the Yelp stars by looking at parent/child
        firstDiv = "div.lemon--div__373c0__1mboc.arrange-unit__373c0__o3tjT"
        innerSpan = "span.lemon--span__373c0__3997G.display--inline__373c0__3JqBP"
        innerDiv = "div.lemon--div__373c0__1mboc.i-stars__373c0__1T6rz"
        somediv = yelpsoup.select(f'{firstDiv} > {innerSpan} > {innerDiv}')

        # scraping first 20 reviews per page
        for x in range(1, 21):
            yelp_stars.append(somediv[x]['aria-label'])

    # Close the browser
    browser.quit()

    yelp_scrape_results = {"Reviews": yelp_reviews, "Stars": yelp_stars}
    
    #this print works, but not when it's called outside the function..
    #print(yelp_scrape_results)

    #return yelp_reviews, yelp_stars
    return yelp_scrape_results


url = 'https://www.yelp.com/biz/mamak-doraville-3?adjust_creative=Yba0SJQtkua4MCvdfFfUrg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Yba0SJQtkua4MCvdfFfUrg'

results = scrape(url)
print(results)
print(type(results))

results = scrape(url)
results = pd.DataFrame(results)
results.to_csv("results_csv", index = False)