import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pymongo
from scrape_mars import scrape
from flask import Flask, jsonify, render_template, redirect, url_for


#################################################
# Database Setup
#################################################
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """This is our Mars Scraping Project."""

    db = client.missionToMarsDB
    collection = db.scrape

    data = collection.find_one()

    return render_template ('home.html', data=data)



@app.route("/scrape")
def scrape_route():

    client.drop_database("missionToMarsDB")
    db = client.missionToMarsDB
    collection = db.scrape

    scrape_results = scrape()

    collection.insert_one(scrape_results)

    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)