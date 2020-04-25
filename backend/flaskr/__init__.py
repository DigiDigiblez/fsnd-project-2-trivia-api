import os
import sys
from random import choice

from flask import Flask, request, abort, jsonify
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

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route('/')
    def index():
        return "Welcome to Carl's Trivia App API!"

    @app.route("/categories", methods=["GET"])
    def get_categories():
        questions = Question.query.all()

        categories = set()
        for question in questions:
            category_type = find_category_type(question.category)
            categories.add(category_type)

        return jsonify({
            "categories": list(categories),
            "total_categories": len(categories),
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
    # GET all existing questions
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

    # TODO TEST: When you click the trash icon next to a question, the question will be removed.
    #   This removal will persist in the database and when you refresh the page.
    # DELETE an existing question (via its ID)
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

    # TODO TEST: When you submit a question on the "Add" tab,
    #       the form will clear and the question will appear at the end of the last page
    #       of the questions list in the "List" tab.

    # POST a new question
    @app.route("/questions", methods=["POST"])
    def post_question():
        try:
            new_question_data = request.get_json()

            # Retrieve the parts of the question from the body
            question_text = new_question_data.get('question', None)
            answer_text = new_question_data.get('answer', None)
            category = new_question_data.get('category', None)
            difficulty = new_question_data.get('difficulty', None)

            # Build a new question object
            new_question = Question(
                question=question_text,
                answer=answer_text,
                category=category,
                difficulty=difficulty
            )

            # Insert it into the db
            new_question.insert()

            return jsonify({
                "success": True,
                "message": "Question successfully added."
            })
        except:
            # Throw: Internal Server Error
            abort(500)

    # TODO TEST: Search by any phrase. The questions list will update to include
    #   only question that include that string within their question.
    #   Try using the word "title" to start.
    # POST a search for a question
    @app.route("/search", methods=["POST"])
    def search_question():
        try:
            search_data = request.get_json()
            search_term = search_data.get('searchTerm', None)

            # If search is blank, show all questions to user (to allow them to reset search)
            if search_term == '' or search_term is None:
                all_questions = Question.query.all()
                formatted_matched_questions = [question.format() for question in all_questions]

                return jsonify({
                    "current_category": None,
                    "questions": formatted_matched_questions,
                    "total_questions": len(formatted_matched_questions),
                    "success": True
                })

            # User has submitted a search, return all fuzzied results
            else:
                search_pattern = "%{}%".format(search_term)

                fuzzy_matched_questions = (
                    Question
                        .query
                        .filter(Question.question.ilike(search_pattern))
                        .all()
                )

                formatted_matched_questions = [question.format() for question in fuzzy_matched_questions]

                return jsonify({
                    "current_category": None,
                    "questions": formatted_matched_questions,
                    "total_questions": len(formatted_matched_questions),
                    "success": True
                })
        except:
            # Throw: Bad Request Error
            abort(400)

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    # GET all existing questions
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
            # Throw Resource Not Found Error
            abort(404)

        category_questions = Question.query.filter(Question.category == category.id).all()

        formatted_category_questions = [question.format() for question in category_questions]

        return jsonify({
            "current_category": None,
            "questions": formatted_category_questions,
            "total_questions": len(formatted_category_questions),
            "success": True
        })

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

    @app.route("/quizzes", methods=["POST"])
    def get_random_quiz_question():
        body = request.get_json()

        # Retrieve quiz data
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")

        # Error handling
        if previous_questions is None or quiz_category is None:
            abort(400)

        category_id = quiz_category['id']

        random_question = choice(
            Question.query.filter(Question.category == category_id).all()
        )

        current_attempts = 0
        allowed_attempts = 3

        while (current_attempts < allowed_attempts) or (random_question.id in previous_questions):
            random_question = choice(Question.query.all())
            current_attempts += 1

        else:
            return jsonify({
                "question": random_question.format()
            })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request",
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found",
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity",
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error",
        }), 500

    if __name__ == "__main__":
        app.run()

    return app
