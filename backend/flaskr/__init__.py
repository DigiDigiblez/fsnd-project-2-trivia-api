import os
import sys

from flask import Flask, request, abort, jsonify, flash
from flask_cors import CORS

from .find_category_type import find_category_type
from .models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    # TODO: Set up CORS. Allow "*" for origins. Delete the sample route after completing the TODOs
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    # TODO: Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route('/')
    def index():
        return "Welcome to Carl's Trivia App API!"

    # TODO: Create an endpoint to handle GET requests for all available categories.
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            "categories": formatted_categories,
            "total_categories": len(formatted_categories),
            "success": True
        })

    # TODO:
    #   Create an endpoint to handle GET requests for questions,
    #   including pagination (every 10 questions).
    #   This endpoint should return a list of questions,
    #   number of total questions, current category, categories.
    #
    # TODO TEST: At this point, when you start the application
    #   you should see questions and categories generated,
    #   ten questions per page and pagination at the bottom of the screen for three pages.
    #   Clicking on the page numbers should update the questions.
    @app.route("/questions", methods=["GET"])
    def get_questions():
        # Pagination logic
        page = request.args.get("page", 1, type=int)

        # TODO-FIX
        if page <= 0 | page > 100:
            abort(404)

        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = set()
        for question in questions:
            category_type = find_category_type(question.category)
            categories.add(category_type)

        return jsonify({
            "categories": list(categories),
            "current_category": None,
            "questions": formatted_questions[start:end],
            "total_questions": len(formatted_questions),
            "success": True
        })

    # TODO:
    #   Create an endpoint to DELETE question using a question ID.
    #
    # TODO TEST: When you click the trash icon next to a question, the question will be removed.
    #   This removal will persist in the database and when you refresh the page.
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question_by_id(question_id):
        error = False

        try:
            question_to_delete = Question.query.filter(Question.id == question_id).one_or_none()

            if question_to_delete is None:
                abort(404)

            Question.delete(question_to_delete)
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
        finally:
            db.session.close()
            if error:
                abort(500)

        return jsonify({
            "success": True
        })

    """
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """

    """
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    """
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  """

    """
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found",
        }), 404

    if __name__ == "__main__":
        app.run()

    return app
