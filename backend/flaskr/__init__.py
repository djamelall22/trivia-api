import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
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
        Intercept response to add 'Access-Control-Allow' headers
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
      Search questions using the search term
      """
      search_term = request.json.get('searchTerm', '')
      questions = [question.format() for question in Question.query.all() if
                  re.search(search_term, question.question, re.IGNORECASE)]
      return jsonify({
          'questions': questions,
          'total_questions': len(questions)




  return app


 

    
