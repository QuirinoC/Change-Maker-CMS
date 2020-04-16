from mongoengine import Document, StringField,\
                        connect, GeoPointField,\
                        DateTimeField, DecimalField,\
                        ObjectIdField, BooleanField, EmbeddedDocumentListField,\
                        EmbeddedDocument,PointField
import datetime

#TIME STUFF
from datetime import datetime, timedelta

class Evento(Document):
  id = StringField(primary_key=True)
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
  id = StringField(primary_key=True)
  nombre = StringField()
  organizacion = StringField()
  microsemblanza = StringField()
  foto_ponente = StringField()
  logo_organizacion = StringField()

class Ponente(Document):
  id = StringField(primary_key=True)
  nombre = StringField()
  organizacion = StringField()
  microsemblanza = StringField()
  foto_ponente = StringField()
  logo_organizacion = StringField()