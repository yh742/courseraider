import sys, os, qrcode, io
from flask import request, jsonify, url_for, render_template, redirect, send_file

from . import api
from .db_helper import Json2db, activate as act, deactivate as deact, get_question, \
    insert_performance, check_activated, get_performance, delete_question, get_all_performance, get_all_questions
from .bitly import BitlyApi
from instance.config import HOSTNAME


@api.route('/v1/survey/<int:cls_id>', methods=['GET'])
def show_survey(cls_id):
    data = get_question(cls_id)
    if data is None or not check_activated(cls_id):
        return jsonify({'id': cls_id, 'error': 'questions for class id does not exist'}), 400
    title = data['form_schema']['title']
    description = data['form_schema']['description']
    properties = data['form_schema']['properties']
    for key in data['ui_schema']:
        properties[key]['widget'] = data['ui_schema'][key]['ui:widget']
    return render_template('survey.html', cls_id=cls_id, title=title, description=description, props=properties, keys=sorted(properties))


@api.route('/v1/survey/submit/<int:cls_id>', methods=['GET', 'POST'])
def submit_survey(cls_id):
    if request.data is None:
        return render_template('survey_complete', good=False)
    insert_performance(request.form)
    return render_template('survey_complete.html', good=True)


@api.route('/v1/questions', methods=['POST'])
def add_questions():
    """
    Handle POSTS to question
    Save question form templates
    """
    if request.get_json() is None:
        return jsonify({'id': None, 'error': 'missing json data'}), 400
    jdb = Json2db(request.get_json())
    try:
        jdb.insert_cls().insert_question()
    except KeyError:
        return jsonify({'id': jdb.class_id, 'error': 'key error'}), 400
    except Exception as e:
        exc = sys.exc_info()
        return jsonify({'id': jdb.class_id, 'error': str(e.args[0])}), 400
    return jsonify({'id': jdb.class_id, 'error': None}), 201


@api.route('/v1/questions/<int:cls_id>', methods=['GET'])
def get_questions(cls_id):
    """
    Handle GET to question
    Retrieves questions based on class id
    """
    try:
        data = get_question(cls_id)
        if data is None:
            return jsonify({'id': cls_id, 'error': 'questions for class id does not exist'}), 400
    except Exception as e:
        return jsonify({'id': cls_id, 'error': str(e.args[0])}), 400
    return jsonify(data), 200


@api.route('/v1/questions/all', methods=['GET'])
def questions_all():
    """
    Handle get requests to get all the questions
    """
    try:
        return jsonify(get_all_questions()), 200
    except Exception as e:
        return jsonify({'id': '', 'error': str(e.args[0])}), 400


@api.route('/v1/questions/delete/<int:cls_id>', methods=['GET'])
def delete_questions(cls_id):
    """
    Deletes based on class id
    """
    try:
        res = delete_question(cls_id)
        if res:
            return jsonify({'id': cls_id, 'error': ''}), 200
        else:
            return jsonify({'id': cls_id, 'error': 'questions for class id does not exist'}), 400
    except Exception as e:
        return jsonify({'id': cls_id, 'error': str(e.args[0])}), 400


@api.route('/v1/questions/activate/<int:cls_id>', methods=['GET'])
def activate(cls_id):
    """
    Handle get requests to activate survey page
    """
    if not act(cls_id):
        return jsonify({'id': cls_id, 'error': 'class does not exist'}), 400
    else:
        # generate bit.ly link
        url = url_for('api.show_survey', cls_id=cls_id)
        bitly = BitlyApi()
        link = bitly.shorten(HOSTNAME + url)
        if link is None:
            return jsonify({'id': cls_id, 'error': 'bitly link could not be generated'}), 400
        return jsonify({'id': cls_id, 'bitly_link': link, 'error': ''}), 200
        # TODO generate 2d barcode


@api.route('/v1/questions/deactivate/<int:cls_id>', methods=['GET'])
def deactivate(cls_id):
    """
    Handle get requests to activate survey page
    """
    if not deact(cls_id):
        return jsonify({'id': cls_id, 'error': 'class does not exist'}), 400
    else:
        return jsonify({'id': cls_id, 'error': ''}), 200


@api.route('/v1/performance/<int:cls_id>', methods=['GET'])
def performance(cls_id):
    """
    Handle get requests to get performance for specific class
    """
    try:
        res = get_performance(cls_id)
        if not res:
            raise Exception('class id does not exist')
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'id': cls_id, 'error': str(e.args[0])}), 400


@api.route('/v1/performance/all', methods=['GET'])
def performances_all():
    """
    Handle get requests to get all the performances
    """
    try:
        return jsonify(get_all_performance()), 200
    except Exception as e:
        return jsonify({'id': '', 'error': str(e.args[0])}), 400


@api.route('/v1/questions/qrcode', methods=['GET'])
def get_qrcode():
    link = request.args.get('url')
    if link is None:
        return jsonify({'error': 'query parameter must include url'})
    img = qrcode.make(link)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

