# Full Stack Trivia API Backend

## Getting Started
* This app can only run locally. It is not hosted any where.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## Error handling
Errors are returned as JSON objects in the following format
```
{
  "success": False,
  "error": 404,
  "message": "Not found"
}
```
Errors expected to return when the request fails:
* `400`: Bad Request
* `404`: Not Found
* `422`: Unprocessable Entity
* `500`: Internal Server Error

## Endpoints
```
GET '/api/v1/categories'
GET '/api/v1/questions'
GET '/api/v1/categories/<id>/questions'
POST '/api/v1/questions'
POST '/api/v1/questions/phrase'
POST '/api/v1/quizzes'
DELETE '/api/v1/questions/<id>'
```

`GET '/api/v1/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with the following keys:
    * `success`: A bool that shows the response status
    * `code`: HTTP response status code
    * `categories`: An object of `id`: `category_string` key:value pairs
- Sample Request: `curl localhost:5000/api/v1/categories`
- Sample Response:
```
{
    "success": true,
    "code": 200,
    "categories": {
      '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports"
    }
}
```

`GET '/api/v1/questions'`
- Fetches a dictionary that contains one page (10 questions) of questions
- Request Arguments: 
    * `page`: Page number (default is one)
- Returns: A JSON object with the following keys:
    * `success`: A bool that shows the response status.
    * `code`: HTTP response status code
    * `page`: Page number
    * `questions`: An array of objects that contains the questions. The objects have the following keys: `id`, `question`, `answer`, `category` and `difficulty`
    * `total_questions`: Total number of questions
    * `categories`: An object of `id`: `category_string` key:value pairs
- Sample Request: `curl localhost:5000/api/v1/questions`
- Sample Response:
```
{
  "success": true,
  "code": 200, 
  "page": 1,
  "total_questions": 19,
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ]
}
```

`GET '/api/v1/categories/<id>/questions'`
- Fetches a dictionary that contains all the questions with a category equals `id`
- Request Arguments: None
- Returns: A JSON object with the following keys:
    * `success`: A bool that shows the response status.
    * `code`: HTTP response status code
    * `questions`: An array of objects that contains the questions. The objects have the following keys: `id`, `question`, `answer`, `category`, `difficulty`
    * `total_questions`: Total number of questions
    * `current_category`: The `id` of the current category
- Sample Request: `curl localhost:5000/api/v1/categories/1/questions`
- Sample Response:
```
{
  "code": 200, 
  "current_category": "1", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

`POST '/api/v1/questions'`
- Creates a new question
- Request Arguments: A JSON object that contains the data of the question in the following keys:
    * `question`: The body of the question
    * `answer`: The answer of the question
    * `category`: The category of the question
    * `difficulty`: The difficulty of the question
- Returns: A JSON object with the following keys:
    * `success`: A bool that shows the response status.
    * `code`: HTTP response status code
- Sample Request: `curl localhost:5000/api/v1/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who wrote The Cairo Trilogy","answer":"Naguib Mahfouz","category":2, "difficulty":2}'`
- Sample Response:
```
{
  "success": True,
  "code": 201
}
```

`POST '/api/v1/questions/phrase'`
- Searches for all the questions with a specific phrase in it
- Request Arguments: A JSON object with the following keys:
    * `searchTerm`: The phrase we want to search for
- Returns: A JSON object with the following keys:
    * `success`: A bool that shows the response status.
    * `code`: HTTP response status code
    * `questions`: An array of objects that contains the questions. The objects have the following keys: `id`, `question`, `answer`, `category`and `difficulty`
    * `total_questions`: Total number of questions
- Sample Request: `curl -X POST localhost:5000/api/v1/questions/phrase -H "Content-Type: application/json" -d '{"searchTerm":"organ"}'`
- Sample Response:
```
{
  "success": True,
  "code": 200,
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "total_questions": 1
}
```

`POST '/api/v1/quizzes'`
- Creates a quiz. This happens by providing a category and the previous questions, if any, and the API will respond with a new question as the value for the `question` key or `None` if there isn't a suitable question.  
- Request Arguments: A JSON object with the following keys:
    * `quiz_category`: The category of the quiz
    * `previous_questions`: A list of the previous questions in the quiz
- Returns: A JSON object with the following keys:
    * `success`: A bool that shows the response status
    * `code`: HTTP response status code
    * `question`: The new question in the form of a JSON object with the following keys: `id`, `question`, `answer`, `category` and `difficulty`
- Sample Request: `curl localhost:5000/api/v1/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":1},"previous_questions":[]}'`
- Sample Response:
```
{
  "success": True,
  "code": 200,
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }
}
```

`DELETE '/api/v1/questions/<id>'`
- Deletes the question with id = `id`  
- Request Arguments: None
- Returns: A JSON object with the following keys:
    * `success`: A bool that shows the response status
    * `code`: HTTP response status code
- Sample Request: `curl localhost:5000/api/v1/questions/5 -X DELETE`
- Sample Response:
```
{
  "success": True,
  "code": 200
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```