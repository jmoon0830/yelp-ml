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



#Creating functions to webscrapej
# Initialize splinter function
def initiate_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape(yelpurl):
    browser = initiate_browser()

    # Putting reviews into a list
    yelp_reviews = []
    yelp_stars = []
    # start from the first page on yelp and go to the fifth page
    start = 0
    num_pages = 5

    # yelp url
    url = yelpurl + '&start=' + str(start)
    browser.visit(url)
    yelphtml = browser.html
    yelpsoup = BeautifulSoup(yelphtml, 'html.parser') 
    # Find the total number of reviews
    reviews = yelpsoup.find('p', class_='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa- text-size--large__373c0__3t60B')

    total_review_text = reviews.text
    
    if not total_review_text:
        print("Uh oh... there was no total review text.")

    total_reviews_stripped = total_review_text.strip('reviews')

    total_reviews = int(total_reviews_stripped)

    # trying to go figure out if it has over 100 reviews or less
    if total_reviews < 100:
        # Calculate the total number of pages. Rounds down to the number of pages so if a number comes out to 3.5, it rounds down to 3
        num_pages = round(int(total_reviews)/20)
        # Rounds the number of reviews down so if there are 65 reviews, rounds down to 60
        end = round(int(total_reviews)/20)*20
    else: 
        end = 20* num_pages

    # if it has less than 100 reviews, the last page should have the total number of reviews minus the rounded reviews to give the
    # left over ratings
    leftover = total_reviews - end

    # loop through yelp page to scrape the comments
    while (start < end):
        url = yelpurl + '&start=' + str(start)
        print(url)
        browser.visit(url)
        start += 20  
        yelphtml = browser.html
        yelpsoup = BeautifulSoup(yelphtml, 'html.parser')
        #Finding the Yelp stars by looking at parent/child
        firstDiv = "div.lemon--div__373c0__1mboc.arrange-unit__373c0__o3tjT"
        innerSpan = "span.lemon--span__373c0__3997G.display--inline__373c0__3JqBP"
        innerDiv = "div.lemon--div__373c0__1mboc.i-stars__373c0__1T6rz"
        somediv = yelpsoup.select(f'{firstDiv} > {innerSpan} > {innerDiv}')
        # finds all reviews

        allcomment = yelpsoup.find_all('p', class_='lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-')
        
        # Scraping less than 100 reviews
        if total_reviews < 100:

            #has less than 20 reviews
            if num_pages == 0:
                for x in range(1, leftover + 1):
                    yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                for y in range(0,len(allcomment)):    
                    yelp_reviews.append(allcomment[y].text)

            #has less than 40 reviews
            elif num_pages == 1:
                if start == 0:
                    for x in range(1, 21):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)
                else:
                    for x in range(1, leftover + 1):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)  

            #has less than 60 reviews
            elif num_pages == 2:
                if start == (0 or 20):
                    for x in range(1, 21):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)    
                else:
                    for x in range(1, leftover + 1):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text) 
                          
            #has less than 80 reviews
            elif num_pages == 3: 
                if start == (0 or 20 or 40):
                    for x in range(1, 21):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)   
                else:
                    for x in range(1, leftover + 1):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)

            #has less than 100 reviews
            elif num_pages == 4:
                if start == (0 or 20 or 40 or 60):
                    for x in range(1, 21):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)   
                else:
                    for x in range(1, leftover + 1):
                        yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
                    for y in range(0,len(allcomment)):    
                        yelp_reviews.append(allcomment[y].text)   

        # for over 100 reviews
        else:
            for x in range(1, 21):
                yelp_stars.append(somediv[x]['aria-label'].strip('star rating'))
            for y in range(0,len(allcomment)):    
                yelp_reviews.append(allcomment[y].text)
                
    # Close the browser
    browser.quit()
    yelp_scrape_results = {"Reviews": yelp_reviews, "Stars": yelp_stars}
    #yelp_scrape_results = {"Reviews": yelp_reviews}

    return yelp_scrape_results
