import sys
from flask import request, jsonify

from . import api
from . import db_helper


@api.route('/api/v1/questions', methods=['POST'])
def add_questions():
    """
    Handle POSTS to quesiton
    Save question form templates
    """
    if (request.get_json() == None):
        return jsonify({'id': None, 'error': 'missing json data'}), 400
    jdb = db_helper.Json2db(request.get_json())
    try:
        jdb.insert_cls()
        jdb.insert_question()
    except KeyError:
        return jsonify({'id': jdb.class_id, 'error': 'keyerror'}), 400
    except:
        exc = sys.exc_info()
        return jsonify({'id': jdb.class_id, 'error': exc[0] + exc[1] + exc[2]}), 400
    return jsonify({'id': jdb.class_id, 'error': None}), 201


    

