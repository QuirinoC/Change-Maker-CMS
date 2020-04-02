from flask import Flask, jsonify, make_response, request, render_template, Response

from mongoengine import *
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

connection = connect('main-db',
        host='main-db',
        port=27017
        )

@app.route('/', methods=['GET'])
def root():
    return 'Change Maker API for CMS '

@app.route('/hooks', methods=['POST'])
def publish():
    print(request.json, flush=True)
    
    return {'ok': 'ok'}

app.run('0.0.0.0', '8080', debug=True)