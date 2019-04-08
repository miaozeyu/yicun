from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from flask import url_for

import hashlib
import json
from math import ceil

from data_provider_service import DataProviderService

db_engine = 'mysql+mysqldb://root:@localhost/yicun'

DATA_PROVIDER = DataProviderService(db_engine)

PAGE_SIZE = 2

def posting(serialize=True):
    postings = DATA_PROVIDER.get_posting(serialize=serialize)
    # page starts at 1
    page = request.args.get("page")

    if page:
        nr_of_pages = int(ceil(float(len(postings)) / PAGE_SIZE))
        converted_page = int(page)
        if converted_page > nr_of_pages or converted_page <= 0:
            return make_response("", 404)

        from_idx = converted_page * PAGE_SIZE - 2  # page=1 from_idx=0; page=2 from_idx=2; page=3 from_idx=4
        stop_idx = from_idx + PAGE_SIZE  # page=1 stop_idx=2; page=2 stop_idx=4; page=3 stop_idx=6

        postings = postings[from_idx:stop_idx]

    if serialize:
        data = {"postings": postings, "total": len(postings)}
        response = make_response(jsonify(data), 200)

        return response
    else:
        return postings


def posting_by_id(id):
    current_posting = DATA_PROVIDER.get_posting(id, serialize=True)
    if current_posting:
        return jsonify({"posting": current_posting})
    else:
        #
        # In case we did not find the posting by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)


def initialize_database():
    DATA_PROVIDER.init_database()


def fill_database():
    DATA_PROVIDER.fill_database()