import os
import re
from flask import Flask, request, abort, jsonify
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def set_headers(response):
        """
        Add Access-Control-Allow headers
        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        """
        get categories from DB
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return jsonify({
            'categories': categories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Get questions, categories and num of total questions from DB
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        questions = [question.format() for question in Question.query.all()]
        page = int(request.args.get('page', '0'))
        upper_limit = page * 10
        lower_limit = upper_limit - 10
        return jsonify({
            'questions': questions[
                lower_limit:upper_limit] if page else questions,
            'total_questions': len(questions),
            'categories': categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete a question by the question id
        """
        question = Question.query.get(question_id)
        if not question:
            return abort(404, f'question with this id not found: {question_id}')
        question.delete()
        return jsonify({
            'deleted': question_id
        })

    @app.route('/questions', methods=['POST'])
    def post_question():
        """
        Adds a question to DB
        """
        question = request.json.get('question')
        answer = request.json.get('answer')
        category = request.json.get('category')
        difficulty = request.json.get('difficulty')
        if not (question and answer and category and difficulty):
            return abort(400,
                         'question object keys missing from the request '
                         'body')
        question_entry = Question(question, answer, category, difficulty)
        question_entry.insert()
        return jsonify({
            'question': question_entry.format()
        })

    @app.route('/search', methods=['POST'])
    def search():
        """
        Search questions using a search term
        """
        search_term = request.json.get('searchTerm', '')
        questions = [question.format() for question in Question.query.all() if
                     re.search(search_term, question.question, re.IGNORECASE)]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions)
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """
        Get questions from BD and filter the question based on a category
        """
        if not category_id:
            return abort(400, 'category id not valid')
        questions = [question.format() for question in
                     Question.query.filter(Question.category == category_id)]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        """
        Get question for quiz
        """
        previous_questions = request.json.get('previous_questions')
        quiz_category = request.json.get('quiz_category')
        if not quiz_category:
            return abort(400, 'Required keys missing from request body')
        category_id = int(quiz_category.get('id'))
        questions = Question.query.filter(
            Question.category == category_id,
            ~Question.id.in_(previous_questions)) if category_id else \
            Question.query.filter(~Question.id.in_(previous_questions))
        question = questions.order_by(func.random()).first()
        if not question:
            return jsonify({})
        return jsonify({
            'question': question.format()
        })

    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        """
        HTTP error handler for all endpoints
        """
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code

    @app.errorhandler(Exception)
    def exception_handler(error):
        """
        serveur ERROR 
        """
        return jsonify({
            'success': False,
            'error': 500,
            'message': f'Something went wrong: {error}'
        }), 500

    return app
