import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from flask import Flask, render_template
import base64

app = Flask(__name__)

url ="https://unsplash.com/s/photos/nature"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

img_tags = soup.find_all('img')

if not os.path.exists('images'):
    os.makedirs('images')

client = MongoClient("mongodb://localhost:27017/")
db = client.photos
images_collection = db.images

#print("collection + " + str(images_collection.count()))
#print("images + " + str(db.images.count()))

if db.images.count() <= 0:

    for img in img_tags:
        
        img_url = img['src']
        if img_url.startswith('https'):
            if 'alt' in img.attrs:
                filename = os.path.join('images', img['alt'] + '.jpg')
            else:
                filename = os.path.join('images', 'image' + str(img_tags.index(img)) + '.jpg')
            with open(filename, 'wb') as f:
                f.write(requests.get(img_url).content)
                print(f'{filename} saved successfully')

            with open(filename, 'rb') as f:
                image_data = f.read()
                image_name = os.path.basename(filename)

                image = {'name': image_name, 'data': image_data}
                result = images_collection.insert_one(image)
                print(f'{image_name} saved to MongoDB with object ID {result.inserted_id}')

# Define a custom filter to base64-encode data
def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

# Register the filter with the Flask app
app.jinja_env.filters['b64encode'] = b64encode

@app.route('/')
def index():
    images = images_collection.find()

    return render_template('photos.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
  