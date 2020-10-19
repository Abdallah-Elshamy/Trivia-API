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
        self.database_path = "postgres://{}/{}".format('postgres:postgres@localhost:5432', self.database_name)
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

    def test_list_categories(self):
        """GET /api/v1/categories: Test fetching of the categories"""
        res = self.client().get('/api/v1/categories')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["categories"]["1"], "Science")
        
    def test_list_questions(self):
        """GET /api/v1/questions: Test fetching of pages of questions"""
        # Test for the default value (page ==1)
        res = self.client().get('/api/v1/questions')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["page"], 1)
        self.assertEqual(len(json_data["questions"]), 10)
        self.assertEqual(json_data["categories"]["1"], "Science")

        # Test for different page
        res = self.client().get('/api/v1/questions?page=2')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["page"], 2)
        self.assertEqual(json_data["categories"]["1"], "Science")

    def test_list_questions_by_category(self):
        """GET /api/v1/categories/<id>/questions: Test fetching of questions with a specific category"""
        res = self.client().get('/api/v1/categories/1/questions')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["total_questions"], 3)
        self.assertEqual(json_data["current_category"], "1")

    def test_create_questions(self):
        """POST /api/v1/questions: Test creating questions"""
        res = self.client().post('/api/v1/questions', json={
           "question":"Who wrote The Cairo Trilogy","answer":"Naguib Mahfouz","category":2, "difficulty":2
        })
        json_data = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_data["code"], 201)
        self.assertTrue(json_data["success"])

        # Test if the question was added to the database by searching for it
        res = self.client().post('/api/v1/questions/phrase', json={
           "searchTerm":"The Cairo Trilogy"
        })
        json_data = res.get_json()
        self.assertEqual(json_data["questions"][0]["answer"], "Naguib Mahfouz")

    def test_search_questions(self):
        """POST /api/v1/questions/phrase: Test Searching for questions with a specific phrase in it"""
        res = self.client().post('/api/v1/questions/phrase', json={
           "searchTerm":"The Cairo Trilogy"
        })
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])

        # Test if the question was retrieved correctly
        self.assertEqual(json_data["questions"][0]["answer"], "Naguib Mahfouz")

    def test_generate_quizzes(self):
        """POST /api/v1/quizzes: Test generating questions for quizzes"""
        res = self.client().post('/api/v1/quizzes', json={
            # There are only 3 questions in category 1. By this 
            # it is guranteed to get the third one in the quiz
           "quiz_category":{"id":1},"previous_questions":[22,21]
        })
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["question"]["answer"], "The Liver")

        # Test if there is no questions left
        res = self.client().post('/api/v1/quizzes', json={
            # There are only 3 questions in category 1. By this 
            # it is guranteed to get None
           "quiz_category":{"id":1},"previous_questions":[22,21,20]
        })
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["question"], None)

    def test_delete_questions(self):
        """DELETE /api/v1/questions/<id>: Test deleting questions"""
        # Delete a specific question so we can test for it
        res = self.client().delete('/api/v1/questions/10')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data["code"], 200)
        self.assertTrue(json_data["success"])

        # Test if the question removed from the database
        res = self.client().post('/api/v1/questions/phrase', json={
           # Question body for question with id = 10
           "searchTerm":"Which is the only team to play in every soccer World Cup tournament?"
        })
        json_data = res.get_json()
        self.assertEqual(json_data["questions"], [])

    # Test for error handling
    
    def test_bad_request(self):
        """Test 400 (Bad Request) errors"""
        # Missing parameters in the request
        res = self.client().post('/api/v1/questions/phrase')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_data["error"], 400)
        self.assertFalse(json_data["success"])
        self.assertEqual(json_data["message"], "Bad Request")

    def test_not_found(self):
        """Test 404 (Not found) errors"""
        res = self.client().get('/api/v1')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json_data["error"], 404)
        self.assertFalse(json_data["success"])
        self.assertEqual(json_data["message"], "Not found")

    def test_unprocessable_entity(self):
        """Test 422 (Unprocessable Entity) errors"""
        # Delete an element that doesn't exist
        res = self.client().delete('/api/v1/questions/1000')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(json_data["error"], 422)
        self.assertFalse(json_data["success"])
        self.assertEqual(json_data["message"], "Unprocessable Entity")
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()