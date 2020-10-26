#dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_yelp

#create flask setup
app = Flask(__name__)

#establish mongoDB connection w/ pymongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/yelp_app")

#render index.html template using data from Mongo
@app.route("/")
def index():
    #Find data with mongoDB
    yelp = mongo.db.yelp.find_one()

    print(yelp)
    #return template & data
    return render_template("index.html", yelp = yelp)

#trigger scrape fxn
@app.route("/scrape")
def scraper():
    yelp_data=scrape_yelp.scrape()
    mongo.db.yelp.update({}, yelp_data, upsert=True)

    #redirect home
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
