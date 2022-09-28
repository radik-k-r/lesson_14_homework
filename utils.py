import sqlite3
import json


def get_data_from_db(query):
    """Возвращает данные в виде словаря, первая строка будет ключом"""
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute(query)
        records = curs.fetchall()
    return records


def get_value_by_title(title):
    """Возвращает данные по пораметру"""
    sql_query = f""" 
    SELECT title, country, release_year,  listed_in AS genre, description
    FROM netflix
    WHERE title = '{title}' 
    ORDER BY date_added DESC
    LIMIT 1
    """
    result = get_data_from_db(sql_query)
    for item in result:
        return dict(item)


def get_by_period(year1, year2):
    """Выполняет поиск между двумя датами"""
    sql_query = f""" 
    SELECT title, release_year
    FROM netflix
    WHERE release_year BETWEEN {year1} and {year2}
    LIMIT 100
    """
    result = get_data_from_db(sql_query)
    title_list = []
    for item in result:
        title_list.append(dict(item))
    return title_list


def get_value_by_rating(rating):
    rating_dict = {
        "children" : ("G", "G"),
        "family" : ("G", "PG", "PG-13"),
        "adult" : ("R", "NC-17")

    }
    sql_query = f""" 
    SELECT title, rating, description
    FROM netflix
    WHERE rating in {rating_dict.get(rating, ("G", "G"))}
    LIMIT 100
    """
    result = get_data_from_db(sql_query)
    rating_list = []
    for item in result:
        rating_list.append(dict(item))
    return rating_list


def get_value_by_type(genre):
    sql_query = f""" 
    SELECT title, description
    FROM netflix
    WHERE listed_in like '%{genre}%'
    ORDER BY date_added DESC
    LIMIT 10
    """
    result = get_data_from_db(sql_query)
    type_list = []
    for item in result:
        type_list.append(dict(item))
    return type_list


def get_coactors(actor1, actor2):
    sql_query = f""" 
    SELECT *
    FROM netflix
    WHERE "cast" like '%{actor1}%' and "cast" like '%{actor2}%'
    ORDER BY date_added DESC
    LIMIT 10
    """
    result = get_data_from_db(sql_query)
    actor_list = []
    names_dict = {}
    for item in result:
        names = set(dict(item).get("cast").split(", ")) - set([actor1, actor2])

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

    for key, value in names_dict.items():
        if value > 2:
            actor_list.append(key)

    return actor_list


def get_film_names_by_param(film_type, year, genre):
    """Возвращает список названий картин с их описаниями в JSON"""
    sql_query = f""" 
        SELECT *
        FROM netflix
        WHERE type = '{film_type}' and
        release_year = '{year}' and
        listed_in like '%{genre}%'
    """

    result = get_data_from_db(sql_query)
    type_list = []
    for item in result:
        type_list.append(dict(item))

    return json.dumps(type_list, ensure_ascii=False, indent=4)

