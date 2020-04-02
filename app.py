from flask import Flask, jsonify, make_response, request, render_template, Response
from pprint import pprint
from mongoengine import *
import os
from flask_cors import CORS, cross_origin
from functools import wraps
from models import Evento, Lugar, Ponente

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

from dotenv import load_dotenv
load_dotenv(dotenv_path='contentful/.env')
SECRET_KEY = os.getenv("HOOK_SECRET")

connection = connect('change_maker_db',
        host='change_maker_db',
        port=27017
        )

def validate_secret(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        secret = request.headers.get('secret')
        if secret != SECRET_KEY:
            return make_response({"error" : "Invalid request token"})

        return func(*args, **kwargs)
    return decorated

def validate_request(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        request_type = request.json.get('type')
        supported_types = ['Entry', 'DeletedEntry']
        content_type = request.json.get('contentType')
        supported_content_types = ['evento', 'lugar', 'ponente']
        # Validate request type to be Entry or Deleted Entry
        if not request_type or request_type not in supported_types:
            return make_response({'warning' : f'No handler defined for request type {request_type}'})
        # Validate request type to be an accepted type
        if not content_type or content_type not in supported_content_types:
            return make_response({'warning' : f'No handler defined for content type {content_type}'})

        return func(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def root():
    return 'Change Maker API for CMS '

@app.route('/hooks', methods=['POST'])
@validate_secret
@validate_request
def hooks_handler():
    content_type = request.json.get('contentType')
    request_type = request.json.get('type')
    handler = {
        'Entry' : insert_document,
        'DeletedEntry' : delete_document
    }[request.json.get('type')]

    Document = {
        'evento' : Evento,
        'ponente' : Ponente,
        'lugar' : Lugar
    }[content_type]

    return handler(request.json, Document)

def insert_document(req: dict, Document):
    data = req.get('data')
    
    document_id = req.get('id')
    try:
        Document.objects(id=document_id).update_one(**data, upsert=True)
        print(f'Stored document: {document_id}')
        return make_response({'success' : f'Stored document {document_id}'})
    except Exception as e:
        print(f'Failed to store document: {document_id}')
        print(e)
        return make_response({'error' : f'Failed to store document {document_id}'})
    
def delete_document(req: dict, Document):
    document_id = req.get('id')

    try:
        Document.objects(id=document_id).delete()
        return make_response({'success' : f'Deleted document {document_id}'})
    except Exception as e:
        print(f'Cannot delete {document_id}', e)
        return make_response({'error' : f'Cannot delete {document_id}'})

app.run('0.0.0.0', '8080', debug=True)