#Import dependencies

#Flask-related dependencies
from flask import Flask, render_template, jsonify, request
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

#Web scrape function
from scrape import scrape

#ML-code-related dependencies
#from textprocess import text_process
#from ml_model import ml_predictor, positive_words, negative_words
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import string
import operator
from sklearn.feature_extraction.text import CountVectorizer
import pickle

import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize

app = Flask(__name__)

def text_process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

#Loading the model
loaded_model = pickle.load(open("model.pickle", 'rb'))
#loaded_model = pickle.load(open("ml_model/model.pickle", 'rb'))



#Loading the vectorizor
loaded_vectorizor = pickle.load(open("vectorizer.pickle", 'rb'))
#loaded_vectorizor = pickle.load(open("ml_model/vectorizer.pickle", 'rb'))



#Looping through the web-scraped reviews to make predictions
def ml_predictor(web_scrapedf):
    #loaded_model = pickle.load(open('model.pickle', 'rb'))

    # #Loading the model
    # loaded_model = pickle.load(open("model.pickle", 'rb'))
    # #loaded_model = pickle.load(open("ml_model/model.pickle", 'rb'))
    


    # #Loading the vectorizor
    # loaded_vectorizor = pickle.load(open("vectorizer.pickle", 'rb'))
    # #loaded_vectorizor = pickle.load(open("ml_model/vectorizer.pickle", 'rb'))
    

    
    #Creating predictions for each review
    for label, row in web_scrapedf.iterrows():
        text = row['Reviews']
        #print(text)
        text_transform = loaded_vectorizor.transform([text])
        #print(text_transform)[0]
        ml_prediction = loaded_model.predict(text_transform)[0]
        web_scrapedf.at[label, 'ml_predictions'] = ml_prediction

    #Filtering on columns we need 
    scrape_results_df = web_scrapedf[['Reviews', 'ml_predictions']]

    return scrape_results_df

#Function to create positive words for word cloud
def positive_words(scrape_results_df):

    #Creating list of positive words
    positive_wordcloud = scrape_results_df[scrape_results_df['ml_predictions'] == 'Positive']

    positivecv = CountVectorizer(analyzer=text_process)   
    positive_fit=positivecv.fit_transform(positive_wordcloud['Reviews'])

    #creating key value dicitionary pair of counts
    positive_word_list = positivecv.get_feature_names();    
    positive_count_list = positive_fit.toarray().sum(axis=0)   


    positive_words = dict(zip(positive_word_list, positive_count_list))
    positive_sorted = sorted(positive_words.items(), key=operator.itemgetter(1), reverse=True)
    positive_sorted = [(p[0], int(p[1])) for p in positive_sorted]
    positive_sorted = positive_sorted[:49]

    return positive_sorted

#Function to create negative words for word cloud
def negative_words(scrape_results_df):
    
    #Creating the list of negative words
    negative_wordcloud = scrape_results_df[scrape_results_df['ml_predictions'] == 'Negative']

    negativecv = CountVectorizer(analyzer=text_process)   
    negative_fit=negativecv.fit_transform(negative_wordcloud['Reviews'])

    #creating key value dicitionary pair of counts
    negative_word_list = negativecv.get_feature_names();    
    negative_count_list = negative_fit.toarray().sum(axis=0)   


    negative_words = dict(zip(negative_word_list, negative_count_list))
    negative_sorted = sorted(negative_words.items(), key=operator.itemgetter(1), reverse=True)
    negative_sorted = [(n[0], int(n[1])) for n in negative_sorted]
    negative_sorted = negative_sorted[:49]

    return negative_sorted


#home page
@app.route("/")
def index():
    return render_template("index.html")


#API Call route
#This endpoint triggers wiping the recipe DB and sending an API call to populate the DB based on the user's search
@app.route("/api/home/api_call", methods=['GET', 'POST'])
def apipull():
    if request.method == 'POST':  
        search_params = request.json

        input_name = search_params['name']
        input_location = search_params['location']
        print(input_name)

        ##Part 1: Using Yelp Autocomplete to get the restaurant's name
        #Constructing API query for Yelp API Autocomplete
        client_id = "Yba0SJQtkua4MCvdfFfUrg"
        api_key = "xAg1Vq9ZHUJetn_7_V_Q6Y98to85Xq8vIXPesjLSu2DY4TlGtZ15ZdMUdSgHByWrs27p4UtLxik7F24_ga3Cyub545yuL2uXfA4p9supuqkUAY0QXvSkLj_8fCmLX3Yx"
        headers = {'Authorization': f'Bearer {api_key}'}

        
        url = "https://api.yelp.com/v3/autocomplete"
        params = {'text':input_name}
        response_json = requests.get(url,params=params,headers=headers).json()

        #This is the official name for the restaurant
        if response_json["terms"]:    
            first_term = response_json["terms"][0]["text"]

            ##Part 2: Retrieving key info needed, using official name from above to pull the info 
            url = "https://api.yelp.com/v3/businesses/search"
            params = {'term':first_term,'location':input_location}

            #Store in JSON
            response_json2 = requests.get(url,params=params,headers=headers).json()

            # Extracting only the part we need
            restaurant_info = response_json2['businesses'][0]

            ##Part 3: Retrieving review based on business id
            business_id = restaurant_info["id"]
            url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
            params = {'term':first_term,'location':input_location}

            #Store in JSON
            response_json3 = requests.get(url,params=params,headers=headers).json()

            #Extract Reviews
            review_info = response_json3["reviews"]

            #Creating Review Objects
            api_object = {"yelp_api" :restaurant_info,"review_info":review_info}
            
            dump_object = dumps(api_object)

            return dump_object

        else:
            message = "Sorry we don't have that! Try a different search :)"
            final_message1 = dumps(message)
            return final_message1

@app.route("/api/home/ml", methods=['GET', 'POST'])
def ml():
    if request.method == 'POST':
        #print(request.data)   
        search_params = request.json
        print(search_params)


        input_name = search_params['name']
        input_location = search_params['location']

        print(input_name)
        print(input_location)

        ##Part 1: Using Yelp Autocomplete to get the restaurant's name
        #Constructing API query for Yelp API Autocomplete
        client_id = "Yba0SJQtkua4MCvdfFfUrg"
        api_key = "xAg1Vq9ZHUJetn_7_V_Q6Y98to85Xq8vIXPesjLSu2DY4TlGtZ15ZdMUdSgHByWrs27p4UtLxik7F24_ga3Cyub545yuL2uXfA4p9supuqkUAY0QXvSkLj_8fCmLX3Yx"
        headers = {'Authorization': f'Bearer {api_key}'}

        
        url = "https://api.yelp.com/v3/autocomplete"
        params = {'text':input_name}
        response_json = requests.get(url,params=params,headers=headers).json()
        print(response_json)
        

        #This is the official name for the restaurant
    if response_json["terms"]:    
        first_term = response_json["terms"][0]["text"]
        print(first_term)


        ##Part 2: Retrieving key info needed, using official name from above to pull the info 
        url = "https://api.yelp.com/v3/businesses/search"
        params = {'term':first_term,'location':input_location}

        #Store in JSON
        response_json2 = requests.get(url,params=params,headers=headers).json()
        #print(response_json2)

        # Extracting only the part we need
        restaurant_info = response_json2['businesses'][0]
        #print(restaurant_info)
        print(type(restaurant_info))
        print(restaurant_info)

        ##Part 3: web scraping to compile all the reviews

        #Creating URL to be used for web scraping part
        yelp_restaurant_url = restaurant_info["url"]
        print(yelp_restaurant_url)

        #Web scraping
        yelp_scrape_results = scrape(yelp_restaurant_url)


        #Extracting Yelp Star ratings for later
        yelp_stars = yelp_scrape_results['Stars']

        #Convert into a dataframe
        yelp_scrape_df= pd.DataFrame({"Reviews" : yelp_scrape_results['Reviews']})


        #Calling ML functions
        predicted_reviews = ml_predictor(yelp_scrape_df)
        #print(predicted_reviews.head())

        #Generative positive reviews for word cloud
        positive_word_count = positive_words(predicted_reviews)

        #Generating negative reviews for word cloud
        negative_word_count = negative_words(predicted_reviews)


        #Combining objects to send off to JS
        combined_object = {"yelp_api" :restaurant_info, "positive": positive_word_count, "negative": negative_word_count, "yelp_stars" : yelp_stars}
        

        #Dumping object
        final_object = dumps(combined_object)

        #Sending off to JS
        return final_object

    else:
        message = "Uh oh! An error occurred. Please try a different search."
        final_message = dumps(message)
        return final_message
        
if __name__ == "__main__":
    text_process = text_process
    app.run(debug=False)