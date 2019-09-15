# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Initialize your Flask app here
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# Create a route and view function that takes in a dictionary and renders index.html template
@app.route("/")
def index():
    mars = list(db.mars_data.find())
    print(mars)
    return render_template("index.html",mars = mars)

# Create a route for scraping
@app.route('/scrape')
def scrape():
    db.mars_data.drop()
    mars = scrape_mars.scrape()
    print(mars)
    db.mars_data.insert_one(mars)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

