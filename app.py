#Import dependencies

#Flask-related dependencies
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

#Web scrape function
from scrape import scrape

#ML-code-related dependencies
from textprocess import text_process
from ml_model import ml_predictor, positive_words, negative_words
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

# setup mongo connection
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

# connect to mongo db and collection
#db = client.yelpDB
#restaurant = db.yelp


#home page
@app.route("/")
def index():
    return render_template("freebie.html")


#API Call route
#This endpoint triggers wiping the recipe DB and sending an API call to populate the DB based on the user's search
@app.route("/api/home/api_call", methods=['GET', 'POST'])
def apipull():
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
        #print(type(restaurant_info))
        #print(restaurant_info)

        ## insert JSON into MongoDB
        #restaurant.insert_one(restaurant_info)

        ##Part 3: web scraping to compile all the reviews

        #Creating URL to be used for web scraping part
        yelp_restaurant_url = restaurant_info["url"]
        print(yelp_restaurant_url)

        #Web scraping
        yelp_scrape_results = scrape(yelp_restaurant_url)
        #print(yelp_scrape_results)
        #print(type(yelp_scrape_results))

        #Extracting Yelp Star ratings for later
        yelp_stars = yelp_scrape_results['Stars']

        #Convert into a dataframe
        yelp_scrape_df= pd.DataFrame({"Reviews" : yelp_scrape_results['Reviews']})
        #print(yelp_scrape_df)


        #Saving to CSV
        yelp_scrape_df.to_csv("web_scrape_csv", index = False)


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


        #Saving as external file to make easier
        with open('file3.json', 'w') as f:
            json.dump(final_object, f)


        #Sending off to JS
        return final_object

    else:
        message = "Uh oh! An error occurred. Please try a different search."
        final_message = dumps(message)
        return final_message
        
        #return restaurant_info, positive_word_count, negative_word_count
        #return positive_word_count


        #print(type(combined_object))
        #print(type(final_object))

        #checking
        #print(final_object)
        #yelp_api_results = dumps(yelp_api_results)

        #return restaurant_info
        #return yelp_api_results



        #exampletuple = positive_word_count
        #exampletuple = jsonify(exampletuple)
        #return exampletuple

        #need to create a dictionary object, yelp_json = yelp_json (python dictionary jsonified), ml_results = ml_results

        ##jimmys code, keep in different file, import function, give it the url input, put it inside of 
        ###research how to send a jsonified python dictionary back to JS 

        #combine yelp_json and ml_results objects together (object of objects), send that back
       
    #    combined_object= yelp_json, ml_results
    #    return combined_object;
        #return ml_results



        
        # background_img = response_json2["businesses"][0]["image_url"]
        # phone_num = response_json2["businesses"][0]["display_phone"]
        # address = response_json2["businesses"][0]["location"]["address1"]
        # is_closed = response_json2["businesses"][0]["is_closed"]
        # avg_rating = response_json2["businesses"][0]["rating"]

        # print(first_term_url)
        # print(background_img)
        # print(phone_num)
        # print(address)
        # print(is_closed)
        # print(avg_rating)

        # #return first_term_url



        #         ## Pulling what's stored in the JSON from the step above, sending to JS
        # data = list(restaurant.find())
        # data2 = list(restaurant.find())
        
        # yelp_json = dumps(data)
        
        # combined_object = {"object": data + data2}

        # final_object = dumps(combined_object)
        # print(final_object)



        # return final_object

       


        #first_term_url = 


        ###web scrape code in a function, call that function on the yelp url stored in first_term_url

        #feed it into the ML model 
        #Ml model to parse out postive reviews and negative reviews, store each into a 




        #input_location = 'atlanta, ga'


       
        

       
        #return result
        

        # # Establish API Call URL
        # # drop previously generated collection
        # restaurant.drop()
        
        # # Constructing Query
        # url = "https://api.edamam.com/search?"
        # query = f"q={search_param['query']}" #this is where keyword search will go
        # api_key = f"&app_id={config.api_id}&app_key={config.api_key}"
        # diet = f"&diet={search_param['diet']}"
        # calories= f"&calories={search_param['calories']}"
        # index = f"&from=0&to=100"
        # query_url = url + query + api_key + diet + calories +index
        # health_list= search_param['health']
        # for label in health_list:
        #     query_url = query_url + f'&health={label}'
        # try:
        #     # Make request
        #     data = requests.get(query_url)
        #     # Store in JSON
        #     data_json = data.json()
        #     recipe_hits = data_json['hits']
        #     for i in range(len(recipe_hits)):
        #         recipe = recipe_hits[i]['recipe']
        #         total_nurtrients = recipe['totalNutrients']
        #         for key, value in total_nurtrients.items(): 
        #             if "." in key:
        #                 new_key = "SUGAR added"
        #                 old_key = "SUGAR.added"
        #                 total_nurtrients[new_key] = total_nurtrients.pop(old_key)
        #     #insert JSON into MongoDB
        #     recipes.insert_many(recipe_hits)

        # except:
        # print("error")
        # data = list(recipes.find())
        # recipe_json = dumps(data)
        # return recipe_json
        # # render an index.html template and pass it the data you retrieved from the database
    #return render_template("freebie.html", data = results)

# #API Call route
# #This endpoint triggers wiping the recipe DB and sending an API call to populate the DB based on the user's search
# @app.route("/api/home/api_call", methods=['GET', 'POST'])
# def apipull():
#     if request.method == 'POST':   
#         search_param = request.json
#         print(search_param)

#         # Establish API Call URL
#         # drop previously generated collection
#         restaurant.drop()
        
#         # Constructing Query
#         url = "https://api.edamam.com/search?"
#         query = f"q={search_param['query']}" #this is where keyword search will go
#         api_key = f"&app_id={config.api_id}&app_key={config.api_key}"
#         diet = f"&diet={search_param['diet']}"
#         calories= f"&calories={search_param['calories']}"
#         index = f"&from=0&to=100"
#         query_url = url + query + api_key + diet + calories +index
#         health_list= search_param['health']
#         for label in health_list:
#             query_url = query_url + f'&health={label}'
#         try:
#             # Make request
#             data = requests.get(query_url)
#             # Store in JSON
#             data_json = data.json()
#             recipe_hits = data_json['hits']
#             for i in range(len(recipe_hits)):
#                 recipe = recipe_hits[i]['recipe']
#                 total_nurtrients = recipe['totalNutrients']
#                 for key, value in total_nurtrients.items(): 
#                     if "." in key:
#                         new_key = "SUGAR added"
#                         old_key = "SUGAR.added"
#                         total_nurtrients[new_key] = total_nurtrients.pop(old_key)
#             #insert JSON into MongoDB
#             recipes.insert_many(recipe_hits)

#         except:
#         print("error")
#         data = list(recipes.find())
#         recipe_json = dumps(data)
#         return recipe_json
#         # # render an index.html template and pass it the data you retrieved from the database
#         # return render_template("index.html", recipe = data)



# #route to load the last page based on the recipe id extracted from clicking an image
# @app.route("/final_recipe/<recipe_id>")
# def load_recipe(recipe_id):
#     data = recipes.find_one({"_id" : ObjectId(recipe_id)})
    
    
# # render an index.html template and pass it the data you retrieved from the database
# return render_template("index2.html", recipe = data)


# #brings the final recipe data to JS
# @app.route("/api/final_recipe/<recipe_id>")
# def load_recipe2(recipe_id):
#     print(recipe_id)
#     data = restaurant.find_one({"_id" : ObjectId(recipe_id)})
#     print(data)
#     recipe_json = dumps(data) 
#     return recipe_json



if __name__ == "__main__":

    app.run(debug=True)