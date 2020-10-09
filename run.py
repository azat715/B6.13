import bottle
from bottle import get
from bottle import request, route, run, HTTPError, response
from bottle.ext import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

from wtforms import Form, SelectField, StringField
from wtforms.validators import DataRequired

import json

# путь к базе
DB_PATH = "sqlite:///db/albums.sqlite3"

Base = declarative_base()
eng = create_engine(DB_PATH)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    eng,
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
)

app.install(plugin)

class Album(Base):
    __tablename__ = "album"

    id = Column(Integer, primary_key=True)
    year = Column(Text)
    artist = Column(Text)
    genre = Column(Text)
    album = Column(Text)

    def __repr__(self):
        return (
            "<Album(year='%s', artist='%s', genre='%s',"
            "album='%s)>"
            % (
                self.year,
                self.artist,
                self.genre,
                self.album,
            )
        )
    def as_dict(self):
        return {'artist': self.artist, 'album': self.album, 'year': self.year, 'genre': self.genre,}

def query(db, form):
    type = form.type.data
    value = form.value.data
    return {
        'year': db.query(Album).filter_by(year = value),
        'artist': db.query(Album).filter_by(artist = value),
        'genre': db.query(Album).filter_by(genre = value),
        'album': db.query(Album).filter_by(album = value),
    }.get(type, None)


class GetArtistForm(Form):
    type = SelectField(choices=['year', 'artist', 'genre', 'album'], validate_choice=True, validators=[DataRequired()])
    value = StringField(validators=[DataRequired()])

@app.get('/api/artist')
def artists(db):
    response.content_type = 'application/json'
    if request.query:
        form = GetArtistForm(request.query)
        if form.validate():
            records = query(db, form)
        else:
            return HTTPError(400, f"Ошибка в запросе")
        if records.all():
            res = [record.as_dict() for record in records]
            return json.dumps(res)
        else:
            return HTTPError(404, f'{form.type.data} {form.value.data} не найден.')
    else:  
        records = db.query(Album).group_by(Album.artist).all()
        if records:
            res = [record.artist for record in records]
            return json.dumps(res)
        else:
            return HTTPError(500, f'База данных пуста')


@app.get('/artist')
def get_form_artist():
    return 
        

@app.get('/albums/<artist>')
def find(artist, db):
    records = db.query(Album).filter_by(artist=artist).all()
    if records:
        res = []
        for record in records:
            res.append(record.as_dict())
        response.content_type = 'application/json'
        print(res)
        return json.dumps(res)
    else:
        return HTTPError(404, f'Артист {artist} не найден.')

@app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

app.run(host='localhost', port=8081, reloader=True)