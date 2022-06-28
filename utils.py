import json
import sqlite3


def connection_to_db(sql):
    """
    Соединнение с базой данныйх
    """
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        query = connection.execute(sql).fetchall()

    return query


def search_by_movie(title):
    """
    Поиск по названию.
    Если таких фильмов несколько, выведите самый свежий
    """
    sql = f'''
            SELECT * FROM netflix
            WHERE title == '{title}'
            AND type = 'Movie'
            ORDER by release_year DESC
            LIMIT 1
            '''

    for item in connection_to_db(sql):
        return dict(item)


def search_by_range(param_1, param_2):
    """
    Поиск по диапазону лет выпуска.
    Ограничен вывод 100 тайтлами.
    """
    sql = f'''
            SELECT title, release_year FROM netflix
            WHERE release_year BETWEEN '{param_1}' AND '{param_2}'
            LIMIT 100
            '''

    query_list = []
    for item in connection_to_db(sql):
        query_list.append(dict(item))

    return query_list


def search_by_rating(rating):
    """
    Поиск по рейтингу.
    С группами:
    для детей, для семейного просмотра, для взрослых.
    """
    rating_base = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f'''
            SELECT title, rating, description FROM netflix
            WHERE rating in {rating_base.get(rating, ("R"))}
            '''

    query_list = []
    for item in connection_to_db(sql):
        query_list.append(dict(item))

    return query_list


def search_by_genre(genre):
    """
    Получаем название жанра в качестве аргумента
    и возвращаем 10 самых свежих фильмов в формате json.
    """

    sql = f'''
            SELECT title, description FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10 
            '''

    query_list = []
    for item in connection_to_db(sql):
        query_list.append(dict(item))

    return query_list


def search_by_actors(actor1, actor2):
    """
    Получаем в качестве аргумента имена двух актеров,
    сохраняем всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз.
    """
    sql = f'''
            SELECT "cast" FROM netflix
            WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
            '''
    result = []
    actors_dict = {}
    for item in connection_to_db(sql):
        actors = set(dict(item).get('cast').split(",")) - set([actor1, actor2])

        for actor in actors:
            actors_dict[str(actor).strip()] = actors_dict.get(str(actor).strip(), 0) + 1

    for key, value in actors_dict.items():
        if value >= 2:
            result.append(key)

    return json.dumps(result)


def just_search(type_, release_year_, genre):
    """
    Передаем тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин
    с их описаниями в JSON.
    """
    sql = f'''
            SELECT title, description, listed_in FROM netflix
            WHERE type = '{type_}'
            AND release_year = '{release_year_}'
            AND listed_in LIKE '%{genre}%'
            '''

    query_list = []

    for item in connection_to_db(sql):
        query_list.append(dict(item))

    return json.dumps(query_list)

