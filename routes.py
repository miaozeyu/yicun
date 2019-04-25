from flask import jsonify, render_template

from middleware import initialize_database as init_db
from middleware import fill_database as fill_db
from middleware import posting
from middleware import posting_by_id
from Data_Ingestor.twitter_streaming_producer import startStreaming
from decorators import *

def init_api_routes(app):
    if app:
        app.add_url_rule('/api/postings/<string:id>', 'posting_by_id', posting_by_id, methods=['GET'])
        app.add_url_rule('/api/postings', 'posting', posting, methods=['GET'])
        app.add_url_rule('/api/realtimeposts', 'startStreaming', startStreaming, methods=['GET'])
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})
        app.add_url_rule('/api/initdb', 'initdb', initialize_database)
        app.add_url_rule('/api/filldb', 'filldb', fill_database)

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


def page_index():
    print('index.html')
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@authenticate
def page_initdb(*args, **kwargs):
    print('initdb.html')
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('initdb.html')

@authenticate
def page_filldb(*args, **kwargs):
    print('filldb.html')
    # only by sending this page fiçrst will the client be connected to the socketio instance
    return render_template('filldb.html')



def init_website_routes(app):
    if app:
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])
        app.add_url_rule('/filldb', 'page_filldb', page_filldb, methods=['GET'])
        app.add_url_rule('/initdb', 'page_initdb', page_initdb, methods=['GET'])
