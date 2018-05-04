import unittest, datetime, json, os, random
from json import JSONEncoder
from flask_testing import TestCase
from flask import abort, url_for, jsonify

# use absolute import
from app import create_app, db
from app.models import Class, Question, Performance


# run from top level directory python3 -m app.test.api_test
class TestBase(TestCase):

    data = {
        'class_id': 12,
        'ui_schema': {
            'Question1': {
                'ui:widget': 'radio'
            },
            'Question2': {
                'ui:widget': 'textarea'
            }
        },
        'form_schema': {
            'title': 'A simple feedback form',
            'description': 'Provide feedback for a class',
            'type': 'object',
            'properties': {
                'Question1': {
                    'type': 'string',
                    'title': 'Question 1',
                    'enum': ['1', '2', '3', '4', '5']
                },
                'Question2': {
                    'type': 'string',
                    'title': 'Feedback',
                }
            }
        }
    }

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        return app

    def setUp(self):
        db.create_all()

    def insertFake(self):
        target_url = url_for('api.add_questions')
        return self.client.post(target_url,content_type='application/json',
                                data=json.dumps(TestApi.data, skipkeys=True))

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestApi(TestBase):

    def test_question_post(self):
        response = self.insertFake()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Class.query.count(), 1)
        self.assertEqual(Question.query.count(), 2)

    def test_question_post_twice(self):
        self.insertFake()
        target_url = url_for('api.add_questions')
        response = self.client.post(target_url, content_type='application/json',
                                    data=json.dumps(TestApi.data, skipkeys=True))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Class.query.count(), 1)
        self.assertEqual(Question.query.count(), 2)

    def test_questions_delete(self):
        self.insertFake()
        target_url = url_for('api.delete_questions', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Class.query.count(), 0)

    def test_question_get(self):
        self.insertFake()
        # compare with this copy
        data = jsonify(TestApi.data).data
        # get questions
        target_url = url_for('api.get_questions', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.maxDiff = 2000
        self.assertEqual(response.data, data)

    def test_question_all_get(self):
        self.insertFake()
        TestApi.data['class_id'] = 11
        self.insertFake()
        # get questions
        target_url = url_for('api.questions_all')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_question_get_missing(self):
        self.insertFake()
        # get questions from a missing class id
        target_url = url_for('api.get_questions', cls_id=1)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 400)

    def test_activate(self):
        self.insertFake()
        # get questions from a missing class id
        target_url = url_for('api.activate', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Class.query.get(TestApi.data['class_id']).active, True)

    def test_deactivate(self):
        self.insertFake()
        # get questions from a missing class id
        target_url = url_for('api.deactivate', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Class.query.get(TestApi.data['class_id']).active, False)

    def test_survey(self):
        self.insertFake()
        target_url = url_for('api.show_survey', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_survey_submit(self):
        self.insertFake()
        target_url = url_for('api.submit_survey', cls_id=TestApi.data['class_id'])
        response = self.client.post(target_url, data={'id-1': '3', 'id-2': 'blahblahblah'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Performance.query.count(), 2)

    def test_get_performance(self):
        self.insertFake()
        target_url = url_for('api.submit_survey', cls_id=TestApi.data['class_id'])
        with open('sentences.txt') as f:
            for line in f.readlines():
                data = dict()
                data['id-1'] = random.randint(1,5)
                data['id-2'] = line
                response = self.client.post(target_url, data=data)
                self.assertEqual(response.status_code, 200)
        target_url = url_for('api.performance', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_get_all_performances(self):

        self.insertFake()
        target_url = url_for('api.submit_survey', cls_id=TestApi.data['class_id'])
        with open('sentences.txt') as f:
            for line in f.readlines():
                data = dict()
                data['id-1'] = random.randint(1,5)
                data['id-2'] = line
                response = self.client.post(target_url, data=data)
                self.assertEqual(response.status_code, 200)
        target_url = url_for('api.performances_all')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()