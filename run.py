import flask
from utils import get_value_by_title, get_by_period, get_value_by_rating, get_value_by_type, get_coactors, \
    get_film_names_by_param
import json

app = flask.Flask(__name__)


@app.route('/movie/<title>')
def view_title(title):
    result = get_value_by_title(title)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"
    )


@app.route("/movie/<year1>/to/<year2>")
def view_by_period(year1, year2):
    result = get_by_period(year1, year2)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"
    )


@app.route("/rating/<rating>")
def view_by_rating(rating):
    result = get_value_by_rating(rating)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"
    )


@app.route("/genre/<genre>")
def view_by_type(genre):
    result = get_value_by_type(genre)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"
    )


# Задание 5
print(get_coactors("Rose McIver", "Ben Lamb"))


# Задание 6
print(get_film_names_by_param("Movie", "2019", "Dramas"))


if __name__ == "__main__":
    app.run(debug=True)