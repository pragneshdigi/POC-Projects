# https://medium.com/swlh/web-scraping-with-python-using-beautifulsoup-and-mongodb-6f15f6b04d68

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
import json
import pymongo

app = Flask(__name__)

def scrape_quotes():
    
    print("scrape call")

    more_links = True
    page = 1
    quotes = []

    while(more_links):

        url = 'http://quotes.toscrape.com/page/{page}'
        response = requests.get(f'http://quotes.toscrape.com/page/{page}').text
        soup = BeautifulSoup(response, 'html.parser')

        for item in soup.select('.quote'):
            quote = {}
            quote['text'] = item.select_one('.text').get_text()
            quote['author'] = item.select_one('.author').get_text()

            tags = item.select_one('.tags')

            quote['tags'] = [tag.get_text() for tag in tags.select('.tag')]
            quotes.append(quote)

        next_link = soup.select_one('.next > a')

        #print(f'scraped page {page}')

        if(next_link):
            page += 1
        else:
            more_links = False

    client = pymongo.MongoClient('mongodb+srv://pragneshdigi:pragnesh123@cluster0.qjike7t.mongodb.net/test',ssl=True,ssl_cert_reqs="CERT_NONE")

    db = client.db.quotes
    
    try:
        db.insert_many(quotes)
        print(f'inserted {len(quotes)} articles')
    except:
        print('an error occurred quotes were not stored to db132')

    
    return quotes
    #print(quotes)                                                                          

    

#client = pymongo.MongoClient('mongodb+srv://pragneshdigi:pragnesh123@cluster0.qjike7t.mongodb.net/test',ssl=True,ssl_cert_reqs="CERT_NONE")
#client = pymongo.MongoClient("mongodb://localhost:27017/")  

'''
# Access database  
mydatabase = client['Students']  
    
# Access collection of the database  
collection=mydatabase['studentscores']  
data = [ 
    {"user":"Krish", "subject":"Database", "score":80}, 
    {"user":"Amit",  "subject":"JavaScript", "score":90}, 
    {"user":"Amit",  "title":"Database", "score":85}, 
    {"user":"Krish",  "title":"JavaScript", "score":75}, 
    {"user":"Amit",  "title":"Data Science", "score":60},
    {"user":"Krish",  "title":"Data Science", "score":95}] 
  
collection.insert_many(data) 

'''

    

# Route for displaying data
@app.route('/')
def display_data():
    
    client = pymongo.MongoClient('mongodb+srv://pragneshdigi:pragnesh123@cluster0.qjike7t.mongodb.net/test',ssl=True,ssl_cert_reqs="CERT_NONE")
    db = client['db']
    collection = db['quotes']
    #data = collection.find_one()
    data = collection.find()
    
    print("display call")
    
    return render_template('index.html', data=data)

  

data123 = {
    'name' : 'John Doe',
    'age': 30,
    'email': 'johndoe@example.com'
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data123)

if __name__ == '__main__':

    print("main call")
    data = scrape_quotes()    
   
    app.run()
