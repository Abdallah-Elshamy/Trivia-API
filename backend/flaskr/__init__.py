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


  @app.route('/api/v1/questions/phrase', methods=['POST'])
  def find_question():
    search_term = request.get_json()['searchTerm']
    questions_list = [question.format() for question in Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()]
    return jsonify({
      "questions": questions_list,
      "total_questions": len(questions_list),
    }), 200


 
  @app.route('/api/v1/categories/<id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    questions_list = [question.format() for question in  Question.query.filter(Question.category == id).all()]

    return jsonify({
      "questions": questions_list,
      "total_questions": len(questions_list),
      "current_category": id
    }), 200
    
  @app.route('/api/v1/quizzes', methods=['POST'])
  def make_quiz():
    quiz_data = request.get_json()
    quiz_category = quiz_data["quiz_category"]
    previous_questions = quiz_data["previous_questions"]
    print(previous_questions)
    questions_list = [question.format() for question in  Question.query.filter(Question.category == quiz_category['id']).all()]
    for question in  questions_list:
      if question['id'] not in previous_questions:
        return jsonify({
          "success": True,
          "code": 200,
          "question": question
        }), 200
    return jsonify({
          "success": True,
          "code": 200,
          "question": None
        }), 200

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity"
    }), 422
  return app

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400
  return app

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500


  return app

    