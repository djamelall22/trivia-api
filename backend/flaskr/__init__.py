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
      Creates a dictionary of all categories
      :return: All categories
      """
      categories = {}
      for category in Category.query.all():
          categories[category.id] = category.type
      return jsonify({
          'categories': categories
      })


  return app


 

    
