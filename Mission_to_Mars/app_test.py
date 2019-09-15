# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

client = pymongo.MongoClient()
db = client.mars_db
mars = list(db.mars_data.find())
print(mars)

# Initialize your Flask app here
app = Flask(__name__)


# Create a route and view function that takes in a dictionary and renders index.html template
@app.route("/")
def index():
    
    return render_template("index.html",mars = mars)

@app.route('/scrape')
def scrape():

    mars = scrape_mars.scrape()
    print("\n\n\n")
    db.mars_data.insert_one(mars)
    return "Scrapped data"

if __name__ == "__main__":
    app.run(debug=True)

