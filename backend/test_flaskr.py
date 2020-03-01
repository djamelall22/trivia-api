import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['categories'], dict)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsInstance(data['categories'], dict)

    def test_delete_question(self):
        question_id = 1
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        if res.status_code == 404:
            self.assertEqual(data['success'], False)
        else:
            self.assertEqual(data['deleted'], 1)

    def test_post_question(self):
        sample_question = {
            'question': 'Who invented the personal computer?',
            'answer': 'Steve Wozniak',
            'category': 4,
            'difficulty': 2
        }
        res = self.client().post('/questions',
                                 data=json.dumps(sample_question),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
