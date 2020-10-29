#Import dependencies
import pandas as pd
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


def text_process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]


#Looping through the web-scraped reviews to make predictions
def ml_predictor(web_scrapedf):

    def text_process(text):
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

    #Loading the model
    loaded_model = pickle.load(open("ml_model/model.pickle", 'rb'))
    
    #Loading the vectorizor
    loaded_vectorizor = pickle.load(open("ml_model/vectorizer.pickle", 'rb'))
    

    #Creating predictions for each review
    for label, row in web_scrapedf.iterrows():
        text = row['Reviews']
        
        text_transform = loaded_vectorizor.transform([text])
        
        ml_prediction = loaded_model.predict(text_transform)[0]
        web_scrapedf.at[label, 'ml_predictions'] = ml_prediction

    #Filtering on columns we need 
    scrape_results_df = web_scrapedf[['Reviews', 'ml_predictions']]

    return scrape_results_df

#Function to create positive words for word cloud
def positive_words(scrape_results_df):

    def text_process(text):
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

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

    def text_process(text):
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    
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
