from flask import request
import psycopg2
from app.models import create_table
from http import HTTPStatus
from psycopg2.errors import UndefinedTable

def create():
    create_table()

    data = request.get_json()

    conn = psycopg2.connect(host="localhost", database="kenzie_series",
    user="maria", password="17122001")

    cur = conn.cursor()

    new_data = {}
    for key, value in data.items():
        if key == 'serie' or key == 'genre':
            new_data[key] = value.title()
        else:
            new_data[key] = value

    serie = (new_data['serie'], new_data['seasons'], new_data['released_date'], new_data['genre'], new_data['imdb_rating'])
    query = 'INSERT INTO ka_series (serie, seasons, released_date, genre, imdb_rating) VALUES (%s, %s, %s, %s, %s)'
    
    cur.execute(query, serie)

    name_serie = (new_data['serie'],)
    select = 'SELECT * FROM ka_series WHERE serie = (%s)'

    cur.execute(select, name_serie)

    registro = cur.fetchall()

    new_data['id'] = registro[0][0]

    conn.commit()

    cur.close()

    return new_data, 201

def series():
    create_table()

    conn = psycopg2.connect(host="localhost", database="kenzie_series",
    user="maria", password="17122001")

    cur = conn.cursor()

    cur.execute("""
        SELECT id, serie, seasons, to_char(released_date, 'DD/MM/YYYY') as released_date, genre, imdb_rating FROM ka_series
    """)

    getting_data = cur.fetchall()

    FIELDNAMES = ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]
    processed_data = [dict(zip(FIELDNAMES, row)) for row in getting_data]

    conn.commit()

    cur.close()

    return {"data": processed_data}, 200

def selec_by_id(serie_id):
    try:
        conn = psycopg2.connect(host="localhost", database="kenzie_series",
        user="maria", password="17122001")

        cur = conn.cursor()

        data = ('DD/MM/YYYY', serie_id)
        select = 'SELECT id, serie, seasons, to_char(released_date, (%s)) as released_date, genre, imdb_rating FROM ka_series WHERE id = (%s)'

        cur.execute(select, data)

        getting_data = cur.fetchall()

        if len(getting_data) == 0:
            return {}, HTTPStatus.NOT_FOUND

        FIELDNAMES = ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]
        processed_data = [dict(zip(FIELDNAMES, row)) for row in getting_data]

        conn.commit()

        cur.close()

        return {"data": processed_data}, 200
    except UndefinedTable:
        create_table()
        return {}, HTTPStatus.NOT_FOUND