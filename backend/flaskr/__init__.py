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

  return app


 

    
