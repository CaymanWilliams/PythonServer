import time
import os
import FBAuto
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename


app = Flask(__name__)
api = Api(app)
uploads_dir = os.path.join(app.instance_path, 'uploads')

@app.route('/facebook/item', methods = ['POST'])
def posting():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        cat = request.form.get('cat')
        condition = request.form.get('condition')
        location = request.form.get('location')
        description = request.form.get('description')
        photos = request.files['photos']

        filename = secure_filename(photos.filename)
        photos.save(os.path.join(uploads_dir, filename))
        photos = os.path.join(uploads_dir, filename)

        toSell = FBAuto.FBItem(name, price, cat, condition, location, description, photos)
        FBAuto.itemPost(toSell)

        return 'OK'

if __name__ == '__main__':
    app.run(port=5005)