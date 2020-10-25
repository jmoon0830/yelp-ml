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

    # Close the browser
    browser.quit()

    #yelp_scrape_results = {"Yelp_Reviews": yelp_reviews}
    yelp_scrape_results = yelp_reviews
    
    #this print works, but not when it's called outside the function..
    #print(yelp_scrape_results)

    return yelp_scrape_results