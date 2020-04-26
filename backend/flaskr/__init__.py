import os
import sys
from math import ceil
from random import choice

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from .find_category_type import find_category_type
from .models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

CODE = {
    # Success codes
    "200_OK": 200,

    # Client error codes
    "400_BAD_REQUEST": 400,
    "404_RESOURCE_NOT_FOUND": 404,
    "405_METHOD_NOT_ALLOWED": 405,
    "422_UNPROCESSABLE_ENTITY": 422,

    # Server error codes
    "500_INTERNAL_SERVER_ERROR": 500
}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route('/', methods=["GET"])
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

    # GET all questions
    @app.route("/questions", methods=["GET"])
    def get_questions():
        # Pagination logic
        page = request.args.get("page", 1, type=int)
        total_questions = len(Question.query.all())
        last_page = ceil(total_questions / QUESTIONS_PER_PAGE)

        if page <= 0 or page > last_page:
            abort(CODE["404_RESOURCE_NOT_FOUND"])

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

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

    # DELETE a question (via it's id)
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        error = False

        try:
            question_to_delete = Question.query.filter(Question.id == question_id).one_or_none()

            Question.delete(question_to_delete)
        except:
            db.session.rollback()
            print(sys.exc_info())
            error = True
        finally:
            db.session.close()

        return jsonify({
            "success": True
        })

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
            abort(CODE["500_INTERNAL_SERVER_ERROR"])

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
            abort(CODE["400_BAD_REQUEST"])

    # GET all existing questions
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
            abort(CODE["404_RESOURCE_NOT_FOUND"])

        category_questions = Question.query.filter(Question.category == category.id).all()

        formatted_category_questions = [question.format() for question in category_questions]

        return jsonify({
            "current_category": None,
            "questions": formatted_category_questions,
            "total_questions": len(formatted_category_questions),
            "success": True
        })

    @app.route("/quizzes", methods=["POST"])
    def get_random_quiz_question():
        body = request.get_json()

        # Retrieve quiz data
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")

        if previous_questions is None or quiz_category is None:
            abort(CODE["400_BAD_REQUEST"])

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
                "question": random_question.format(),
                "success": True
            })

    @app.errorhandler(CODE["400_BAD_REQUEST"])
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": CODE["400_BAD_REQUEST"],
            "message": "Bad request",
        }), CODE["400_BAD_REQUEST"]

    @app.errorhandler(CODE["404_RESOURCE_NOT_FOUND"])
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": CODE["404_RESOURCE_NOT_FOUND"],
            "message": "Resource not found",
        }), CODE["404_RESOURCE_NOT_FOUND"]

    @app.errorhandler(CODE["405_METHOD_NOT_ALLOWED"])
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": CODE["405_METHOD_NOT_ALLOWED"],
            "message": "Method not allowed",
        }), CODE["405_METHOD_NOT_ALLOWED"]

    @app.errorhandler(CODE["422_UNPROCESSABLE_ENTITY"])
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": CODE["422_UNPROCESSABLE_ENTITY"],
            "message": "Unprocessable entity",
        }), CODE["422_UNPROCESSABLE_ENTITY"]

    @app.errorhandler(CODE["500_INTERNAL_SERVER_ERROR"])
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": CODE["500_INTERNAL_SERVER_ERROR"],
            "message": "Internal server error",
        }), CODE["500_INTERNAL_SERVER_ERROR"]

    if __name__ == "__main__":
        app.run()

    return app
