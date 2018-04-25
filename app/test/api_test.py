import unittest, datetime, json
from json import JSONEncoder
from flask_testing import TestCase
from flask import abort, url_for

# use absolute import
from app import create_app, db
from app.models import Class, Question, Performance


# run from top level directory python3 -m app.test.api_test
class TestBase(TestCase):

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestApi(TestBase):

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

    def test_question_post(self):
        target_url = url_for('api.add_questions')
        response = self.client.post(target_url,
            content_type='application/json', data=json.dumps(TestApi.data, skipkeys=True))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Class.query.count(), 1)
        self.assertEqual(Question.query.count(), 2)

    def test_question_post_twice(self):
        target_url = url_for('api.add_questions')
        response = self.client.post(target_url,
            content_type='application/json', data=json.dumps(TestApi.data, skipkeys=True))
        response = self.client.post(target_url,
            content_type='application/json', data=json.dumps(TestApi.data, skipkeys=True))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Class.query.count(), 1)
        self.assertEqual(Question.query.count(), 2)

    def test_question_get(self):
        # post questions
        target_url = url_for('api.add_questions')
        data = json.dumps(TestApi.data, skipkeys=True)
        response = self.client.post(target_url,
            content_type='application/json', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Class.query.count(), 1)
        self.assertEqual(Question.query.count(), 2)

        # get questions
        target_url = url_for('api.get_questions', cls_id=TestApi.data['class_id'])
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.maxDiff = 2000
        self.assertEqual(response.data.decode('utf-8'), data)

    def test_question_get_missing(self):

        # get questions
        target_url = url_for('api.get_questions', cls_id=1)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()