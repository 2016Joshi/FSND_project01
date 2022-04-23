# Backend - Full Stack Trivia API 
This is Trivia API which provides end points for retrieving categories and questions. This provides API for retrieving, adding and deleting questions. Additionally it has support for pagination and retrieving questions based on categories.
### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Endpoints

GET  '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

```json
{
"categories" :{
"1" : "Science",
"2" : "Art",
"3" : "Geography",
"4" : "History",
"5" : "Entertainment",
"6" : "Sports"
},
"success" : true
}

```
GET  '/questions?page=<page_number>'
- Fetches questons and answers based on the page number provided. By default page number is 1.
- Request Arguments(optional): page:int
- Returns: Object with categories with id: category_string as key:value pairs. Also Questions array with id, question, answer, category id and difficulty. It provides total number of questions available as well.
- Example response: 

```json
{
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
     "answer": "Escher", 
     "category": 2, 
     "difficulty": 1, 
     "id": 16, 
     "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
   },  
   {
     "answer": "Mona Lisa", 
     "category": 2, 
     "difficulty": 3, 
     "id": 17, 
     "question": "La Giaconda is better known as what?"
   }
 ], 
 "success": true, 
 "total_questions": 23
}

```

DELETE  '/questions/<question_id>'
- Delete the questions from the repository based on the question id if exists.
- Request Arguments: question_id:int
- Returns: Delete the question from repository and provides response with deleted id.
- Example response: 

```json

{
  "deleted": 54,
  "success": true
}
```

POST  '/questions'
- Creates a new question in the repository. 
- Request Body: {question:string, answer:string, difficulty:int, category:string} (all fields are mandatory)
- Returns: Adds new question to repository and provides response with created question id.
- Example response: 

```json

{
  "created": 55,
  "success": true
}
```

POST  '/questions/search'
- Fetches all questions where a substring matches the search term (not case-sensitive)
- Request Body: {searchterm:string}
- Returns: Matching questions (not case-sensitive)
- Example response: 

```json
{
"questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 11
  }
```

GET  '/categories/<int:category_id>/questions'
- Fetches all questions for the specified category
- Request Arguments: category_id:int
- Returns: Matching questions based on the category selected
- Example response: 

```json
{
"current_category": 6, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
  }
```

POST  '/quizzes'
- Fetches one random question for the seleted category. Previous questions are not asked again.
- Request body: {previous_questions: arr, quiz_category: {id:int, type:string}}
- Returns: Random question and answer with id, category and difficulty
- Example response: 

```json
{
  "question": {
    "answer": "Uruguay", 
    "category": 6, 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
```
## Error Responses
400 - Bad request
404 - Not found
422 - Not processable

Sample error response

```json
{
 "error": 422,
 "success": false
 "message": "Not processable"
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
