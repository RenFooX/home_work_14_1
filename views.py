import json

from flask import Flask

import utils


app = Flask(__name__)


@app.route("/movie/<title>/")
def search_by_title(title):
    """
    Вьюшка для маршрута /movie/<title> ,
    которая бы выводит данные про фильм
    """
    data = utils.search_by_movie(title)
    return app.response_class(response=json.dumps(data))


@app.route("/movie/<param_1>/to/<param_2>/")
def search_by_years(param_1, param_2):
    """
    Вьюшка для маршрута /movie/year/to/year,
    которая бы выводит список словарей.
    """
    data = utils.search_by_range(param_1, param_2)
    return app.response_class(response=json.dumps(data))


@app.route("/rating/<rating>/")
def search_by_rating(rating):
    """ Вьюшку, выведит список словарей,
    содержащий информацию о названии, рейтинге и описании.
    """
    data = utils.search_by_rating(rating)
    return app.response_class(response=json.dumps(data))


@app.route("/genre/<genre>/")
def search_by_genre(genre):
    """
    Вьюшка `/genre/<genre>` которая возвращает список
    содержаться название и описание каждого фильма.
    """
    data = utils.search_by_genre(genre)
    return app.response_class(response=json.dumps(data))


if __name__ == '__main__':
    app.run()
