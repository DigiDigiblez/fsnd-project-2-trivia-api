import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from . import create_app, CODE
from .models import setup_db, Question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Create and insert dummy question into db
        new_question = Question(
            question="Why was 6 afraid of 7?",
            answer="Because 7 8 9...",
            category=1,
            difficulty=1
        )
        new_question.insert()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET '/' endpoint (200)
    def test_200_for_get_index(self):
        """Testing for 200 on the GET '/' endpoint"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data['success'], True)

    # OPTIONS '/' endpoint (405)
    def test_405_for_options_index(self):
        """OPTIONS '/' endpoint (405)"""
        res = self.client().options('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # GET '/categories' endpoint (200)
    def test_200_for_get_categories(self):
        """GET '/categories' endpoint (200)"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data) > 0, True)
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data['total_categories'] > 0, True)

    # GET '/questions' endpoint (200) (1st)
    def test_200_for_get_questions_I(self):
        """GET '/questions' endpoint (200) (1st)"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertTrue(len(data["questions"]))

    # GET '/questions' endpoint (200) (2nd)
    def test_200_for_get_questions_II(self):
        """GET '/questions' endpoint (200) (2nd)"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data['questions']), 10)

    # GET '/questions' endpoint (200) (3rd)
    def test_200_for_get_questions_III(self):
        """GET '/questions' endpoint (200) (3rd)"""
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['questions']) >= 1)  # Page exists, thus should have at least 1 question

    # GET '/questions' endpoint (404) (1st)
    def test_404_for_get_questions_I(self):
        """GET '/questions' endpoint (404) (1st)"""
        res = self.client().get('/questions?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["404_RESOURCE_NOT_FOUND"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # GET '/questions' endpoint (404) (2nd)
    def test_404_for_get_questions_II(self):
        """GET '/questions' endpoint (404) (2nd)"""
        res = self.client().get('/questions?page=777')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["404_RESOURCE_NOT_FOUND"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # DELETE '/questions/<int:question_id>' endpoint (200)
    def test_200_for_delete_question(self):
        """DELETE '/questions/<int:question_id>' endpoint (200)"""
        res = self.client().delete("/questions/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data["success"], True)

    # DELETE '/questions/<int:question_id>' endpoint (404) (1st)
    def test_404_for_delete_question_I(self):
        """DELETE '/questions/<int:question_id>' endpoint (404) (1st)"""
        res = self.client().delete("/questions/-1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["404_RESOURCE_NOT_FOUND"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # DELETE '/questions/<int:question_id>' endpoint (422) (2nd)
    def test_404_for_delete_question_II(self):
        """DELETE '/questions/<int:question_id>' endpoint (422) (2nd)"""
        res = self.client().delete("/questions/77777")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["422_UNPROCESSABLE_ENTITY"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable entity")

    # POST '/questions' endpoint (200)
    def test_200_for_post_question(self):
        """POST '/questions' endpoint (200)"""
        res = self.client().post('/questions', json={"question": "What's surely better than 4 years at university?",
                                                     "answer": "A Udacity Nanodegree", "category": 1, "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data["success"], True)

    # POST '/questions' endpoint (405)
    def test_405_for_post_question(self):
        """POST '/questions' endpoint (405)"""
        res = self.client().post('/questions/1', json={"question": "Should someone POST to this API endpoint?",
                                                       "answer": "Click 'run tests' and find out ;)", "category": 1,
                                                       "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # PUT '/questions' endpoint (405)
    def test_405_for_put_question(self):
        """PUT '/questions' endpoint (405)"""
        res = self.client().put('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # PATCH '/questions' endpoint (405)
    def test_405_for_patch_question(self):
        """PATCH '/questions' endpoint (405)"""
        res = self.client().patch('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # POST '/search' endpoint (200) (1st)
    def test_200_for_post_question_search_I(self):
        """POST '/search' endpoint (200) (1st)"""
        res = self.client().post('/search', json={"searchTerm": "afraid"})  # A question matching "afraid" exists
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'] > 1, True)

    # POST '/search' endpoint (200) (2nd)
    def test_200_for_post_question_search_II(self):
        """POST '/search' endpoint (200) (2nd)"""
        res = self.client().post('/search', json={"searchTerm": "xyz"})  # No question matching "xyz" exists
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    # POST '/search' endpoint (200) (3rd)
    def test_200_for_post_question_search_III(self):
        """POST '/search' endpoint (200) (3rd)"""
        res = self.client().post('/search', json={"searchTerm": ""})  # Blank search conveniently shows all questions
        data = json.loads(res.data)

        total_questions = len(Question.query.all())

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], total_questions)

    # POST '/search' endpoint (400)
    def test_400_for_post_question_search(self):
        """POST '/search' endpoint (400)"""
        res = self.client().post('/search', json=["One", "Two", "Three"])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["400_BAD_REQUEST"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    # DELETE '/search' endpoint (405)
    def test_405_for_delete_question_search(self):
        """DELETE '/search' endpoint (405)"""
        res = self.client().delete('/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # GET '/categories/<int:category_id>/questions' endpoint (200)
    def test_200_for_get_questions_by_category(self):
        """GET '/categories/<int:category_id>/questions' endpoint (200)"""
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data["success"], True)

    # GET '/categories/<int:category_id>/questions' endpoint (404)
    def test_404_for_get_question_by_category_id(self):
        """GET '/categories/<int:category_id>/questions' endpoint (404)"""
        res = self.client().get("/categories/-1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["404_RESOURCE_NOT_FOUND"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # POST '/categories/<int:category_id>/questions' endpoint (405)
    def test_404_for_get_question_by_category_id(self):
        """POST '/categories/<int:category_id>/questions' endpoint (405)"""
        res = self.client().post("/categories/-1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # DELETE '/categories/<int:category_id>/questions' endpoint (405)
    def test_404_get_question_by_category_id(self):
        """DELETE '/categories/<int:category_id>/questions' endpoint (405)"""
        res = self.client().delete("/categories/-1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # POST '/quizzes' endpoint (200)
    def test_200_for_post_quiz_question(self):
        """POST '/quizzes' endpoint (200)"""
        res = self.client().post('/quizzes', json={"previous_questions": [],
                                                   "quiz_category": {"type": "Sports", "id": "2"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["200_OK"])
        self.assertEqual(data["success"], True)

    # POST '/quizzes' endpoint (400)
    def test_400_for_post_quiz_question(self):
        """POST '/quizzes' endpoint (400)"""
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["400_BAD_REQUEST"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    # GET '/quizzes' endpoint (405)
    def test_405_for_get_quiz(self):
        """GET '/quizzes' endpoint (405)"""
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, CODE["405_METHOD_NOT_ALLOWED"])
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
