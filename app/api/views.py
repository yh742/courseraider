import sys, json
from flask import request, jsonify, Response

from . import api
from . import db_helper


@api.route('/api/v1/questions', methods=['POST'])
def add_questions():
    """
    Handle POSTS to question
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


@api.route('/api/v1/questions/<int:cls_id>')
def get_questions(cls_id):
    """
    Handle GET to quesiton
    Retrieves questions based on class id
    """
    try:
        data = db_helper.Db2json().get_question(cls_id)
        if data == None:
            return jsonify({'id': cls_id, 'error': 'class id does not exist'}), 400
    except:
        exc = sys.exc_info()
        return jsonify({'id': cls_id, 'error': exc[0] + exc[1] + exc[2]}), 400
    return Response(json.dumps(data), status=200, mimetype='application/json')



    

