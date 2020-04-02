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

def validate_contentful(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        secret = request.headers.get('secret')
        if secret == SECRET_KEY:
            return func(*args, **kwargs)
        else:
            return make_response({"error" : "Invalid request token"})
    return decorated

@app.route('/', methods=['GET'])
def root():
    return 'Change Maker API for CMS '

@app.route('/hooks', methods=['POST'])
@validate_contentful
def hooks_handler():
    request_type = request.json.get('type')
    supported_types = ['Entry', 'DeletedEntry']
    # Validate request type to be Entry or Deleted Entry
    if not type or request_type not in supported_types:
        return make_response({'warning' : 'No handler defined for request type [Nothing done]'})

    handler = {
        'Entry' : insert_document,
        'DeletedEntry' : delete_document
    }[request_type]
    print(request.json)
    return handler(request.json)

def normalize_fields(fields: dict):
    for key in fields:
        pass

def insert_document(req: dict):
    content_type = req.get('contentType')
    supported_content_types = ['evento', 'lugar', 'ponente']
    if not content_type or content_type not in supported_content_types:
        return make_response({'warning' : 'No handler defined for content type [Nothing done]'})

    fields = req.get('fields')
    
    handler_document = {
        'evento' : insert_event,
        'ponente' : insert_ponente,
        'lugar' : insert_lugar
    }[content_type]
    handler_document(1 ,fields)
    return {'ok': 'inserted document'}

def insert_event(id, fields):
    '''Evento(
        idEvento = id,
        titulo = fields.get('titulo')
        fecha = 
        hora = 
        lugar = 
        ponente = 
        tipo = 
        duracion = 
        aforo = 
        categoria = 
        etapa = 
        descripcion_corta =
        descripcion_completa =
        foto_evento = 
    ).save()
    '''
    return True
def insert_ponente(fields):
    Ponente(

    ).save()
    return True
def insert_lugar(fields):
    Lugar(

    ).save()
    return True

def delete_document(req: dict):
    print('delete')
    return {'ok' : 'deleted document'}

app.run('0.0.0.0', '8080', debug=True)