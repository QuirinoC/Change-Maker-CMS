from mongoengine import Document, StringField,\
                        connect, GeoPointField,\
                        DateTimeField, DecimalField,\
                        ObjectIdField, BooleanField, EmbeddedDocumentListField,\
                        EmbeddedDocument,PointField
import datetime

#TIME STUFF
from datetime import datetime, timedelta

class Evento(Document):
  idEvento = StringField()
  titulo = StringField()
  fecha = StringField()
  hora = StringField()
  lugar = StringField()
  ponente = StringField()
  tipo = StringField()
  duracion = StringField()
  aforo = StringField()
  categoria = StringField()
  etapa = StringField()
  descripcion_corta = StringField()
  descripcion_completa = StringField()
  foto_evento = StringField()

class Lugar(Document):
  idLugar = StringField()
  nombre = StringField()
  organizacion = StringField()
  microsemblanza = StringField()
  foto_ponente = StringField()
  logo_organizacion = StringField()

class Ponente(Document):
  idPonente = StringField()
  nombre = StringField()
  organizacion = StringField()
  microsemblanza = StringField()
  foto_ponente = StringField()
  logo_organizacion = StringField()

'''
class Session(Document):
    userID          = StringField(required=True)
    created_at      = DateTimeField(default=datetime.utcnow)
    expires_at      = DateTimeField(default=create_expire)
    session_hash    = StringField(required=True)

class Location(Document):
    userID          = GeoPointField(required=True)
    uame            = StringField(required=False, default='current')
    description     = StringField(required=False)

class Product(EmbeddedDocument):
    name            = StringField(required=True)
    price           = DecimalField(required=True)
    category        = StringField(required=True) 

class Cart(Document):
    userID          = ObjectIdField(required=True)
    restaurantID    = ObjectIdField(required=True)
    products        = EmbeddedDocumentListField(Product)
'''