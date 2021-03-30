import time
import os
import FBAuto
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename


app = Flask(__name__) #initialize app
api = Api(app) #initialize api handler

uploads_dir = os.path.join(app.instance_path, 'uploads') #specify where uploads are to be located

@app.route('/facebook/item', methods = ['POST']) #define the route
def posting(): #handler for the specific route
    if request.method == 'POST':
        #get the required fields
        user = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get('name')
        price = request.form.get('price')
        cat = request.form.get('cat')
        condition = request.form.get('condition')
        location = request.form.get('location')
        description = request.form.get('description')
        photos = request.files['photos']

        #handles the pciture upload
        filename = secure_filename(photos.filename)
        photos.save(os.path.join(uploads_dir, filename))
        photos = os.path.join(uploads_dir, filename)

        #calls the automation methods
        toSell = FBAuto.FBItem(name, price, cat, condition, location, description, photos)
        FBAuto.itemPost(toSell, user, password)

        return 'OK'

#run server
if __name__ == '__main__':
    app.run(port=5005)