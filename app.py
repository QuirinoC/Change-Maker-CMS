from flask import Flask, jsonify, make_response, request, render_template, Response

from mongoengine import *
import os
from flask_cors import CORS, cross_origin
from functools import wraps

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

connection = connect('main-db',
        host='main-db',
        port=27017
        )

def validate_contentful(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        secret = request.headers.get('secret')
        print('Secret', secret)
        return func(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def root():
    return 'Change Maker API for CMS '

@app.route('/hooks', methods=['POST'])
@validate_contentful
def publish():
    print(request.json)
    return {'ok': 'ok'}

app.run('0.0.0.0', '8080', debug=True)