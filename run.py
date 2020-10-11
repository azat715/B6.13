import json
import logging

import bottle
from bottle import HTTPError, get, request, response, run, static_file, template
from bottle.ext import sqlalchemy
from loguru import logger
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from wtforms import Form, SelectField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

DB_PATH = "sqlite:///db/albums.sqlite3" # путь к базе

Base = declarative_base()
eng = create_engine(DB_PATH)

app = bottle.Bottle() #создание app bottle

# настройка плагина bottle.ext sqlalchemy
plugin = sqlalchemy.Plugin(
    eng,
    keyword="db",  # Keyword used to inject session database in a route (default 'db').
    commit=True,  # If it is true, plugin commit changes after route is executed (default True).
)

app.install(plugin) # установка плагина


class Album(Base):
    __tablename__ = "album"

    id = Column(Integer, primary_key=True)
    year = Column(Text)
    artist = Column(Text)
    genre = Column(Text)
    album = Column(Text, unique = True)

    def __repr__(self):
        return "<Album(year='%s', artist='%s', genre='%s'," "album='%s)>" % (
            self.year,
            self.artist,
            self.genre,
            self.album,
        )

    def as_dict(self):
        """
        возврат словаря из строки базы данных
        """
        return {
            "artist": self.artist,
            "album": self.album,
            "year": self.year,
            "genre": self.genre,
        }


def query(db, form):
    """
    создание запроса к базе данных
    """
    type = form.type.data
    value = form.value.data
    return {
        "year": db.query(Album).filter_by(year=value),
        "artist": db.query(Album).filter_by(artist=value),
        "genre": db.query(Album).filter_by(genre=value),
        "album": db.query(Album).filter_by(album=value),
    }.get(type, None)


class GetArtistForm(Form):
    """
    wtforms  валидация формы запроса к базе данных 
    """
    type = SelectField(
        choices=["year", "artist", "genre", "album"],
        validate_choice=True,
        validators=[DataRequired()],
    )
    value = StringField(validators=[DataRequired()])


class NewArtistForm(Form):
    """
    wtforms  валидация формы запроса к базе данных 
    """
    # ["year", "artist", "genre", "album"],
    artist = StringField(validators=[DataRequired(), Length(1, 50)])
    album = StringField(validators=[DataRequired(), Length(1, 50)])
    year = IntegerField(validators=[DataRequired(), NumberRange(1900, 2050)])
    genre = StringField(validators=[DataRequired(), Length(1, 50)])


@app.get("/api/artist")
def artists(db):
    """
    точка доступа api к базе данных 
    пример запроса /api/artist?type=artist&value=Beatles 
    """
    response.content_type = "application/json"
    if request.query:
        form = GetArtistForm(request.query.decode())
        if form.validate():
            records = query(db, form)
        else:
            return HTTPError(400, f"Ошибка в запросе")
        if records.all():
            res = [record.as_dict() for record in records]
            return json.dumps(res)
        else:
            return HTTPError(404, f"{form.type.data} {form.value.data} не найден.")
    else:
        records = db.query(Album).group_by(Album.artist).all()
        if records:
            res = [record.artist for record in records]
            return json.dumps(res)
        else:
            return HTTPError(500, f"База данных пуста")


@app.get("/artist")
def get_form_artist(db):
    """
    форма запроса с помощью form html
    """
    if request.query:
        form = GetArtistForm(request.query.decode())
        if form.validate():
            records = query(db, form)
        else:
            return HTTPError(400, f"Ошибка в запросе")
        if records.all():
            info = {"title": "Результаты запроса", "records": records}
            return template("res.tpl", info)
        else:
            return HTTPError(404, f"{form.type.data} {form.value.data} не найден.")
    else:
        return template("query.tpl")

@app.get("/new_artist")
def get_form_new():
    """
    форма запроса новый артист html
    """
    return template("new_artist.tpl")

@app.post("/new_artist")
def new_artist(db):
    artist = Album()
    if request.forms:
        form = NewArtistForm(request.forms.decode())
        if form.validate():
            form.populate_obj(artist)
            q = db.query(Album).filter(Album.album == artist.album)
            if not db.query(q.exists()).scalar():
                db.add(artist)
                content = {"message": "Запись добавлена в базу данных"}
                return template("message.tpl", content)
            else:
                content = {"message": "Дубликат записи не добавлен в базу данных"}
                return template("message.tpl", content)
        
        else:
            return HTTPError(400, f"Ошибка в запросе")
    else:
        return HTTPError(400, f"Ошибка сервера")



@app.get("/css/<filename>")
def stylesheets(filename):
    """
    точка доступа к css 
    """
    return static_file(filename, root="./assets/css/")


app.run(host="localhost", port=8081, reloader=True)
