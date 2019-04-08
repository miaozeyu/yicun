from flask import jsonify

from middleware import initialize_database as init_db
from middleware import fill_database as fill_db
from middleware import posting
from middleware import posting_by_id


def init_api_routes(app):
    if app:
        app.add_url_rule('/api/postings/<string:id>', 'posting_by_id', posting_by_id, methods=['GET'])
        app.add_url_rule('/api/postings', 'posting', posting, methods=['GET'])
        app.add_url_rule('/api/initdb', 'initdb', initialize_database)
        app.add_url_rule('/api/filldb', 'filldb', fill_database)
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})


def initialize_database():
    message_key = "Initialize Database"
    try:
        init_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))

    return jsonify(build_message(message_key, "OK"))


def fill_database():
    message_key = "Fill Database"
    try:
        fill_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))

    return jsonify(build_message(message_key, "OK"))


def build_message(key, message):
    return {key:message}


def list_routes(app):
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})


