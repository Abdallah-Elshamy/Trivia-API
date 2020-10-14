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
  
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST, OPTIONS')
    return response


  @app.route('/api/v1/categories', methods=['GET'])
  def list_categories():
    categories = {}
    for category in  Category.query.all():
      categories[category.id] = category.type
    return jsonify({
      "success": True,
      "code": 200,
      "categories": categories
    }), 200

  @app.route('/api/v1/questions', methods=['GET'])
  def list_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE 
    questions_list = [question.format() for question in  Question.query.all()]
    categories = {}
    for category in  Category.query.all():
      categories[category.id] = category.type
    return jsonify({
      "success": True,
      "code": 200,
      "page": page,
      "questions": questions_list[start:end],
      "total_questions": len(questions_list),
      "categories": categories
    }), 200

  @app.route('/api/v1/questions/<id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.get(id)
    try: 
      question.delete()
      return jsonify({
        "success": True,
        "code": 200,
      }), 200
    except:
      abort(422)

  @app.route('/api/v1/questions', methods=['POST'])
  def add_question():
    question_data = request.get_json()
    question = Question(question_data['question'], question_data['answer'],
                        question_data['category'], question_data['difficulty'])
    try:
      question.insert()    
      return jsonify({
        "success": True,
        "code": 201
      }), 201
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''


 
  @app.route('/api/v1/categories/<id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    questions_list = [question.format() for question in  Question.query.filter(Question.category == id).all()]

    return jsonify({
      "questions": questions_list,
      "total_questions": len(questions_list),
      "current_category": id
    }), 200
    
  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    