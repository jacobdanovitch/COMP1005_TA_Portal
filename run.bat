set FLASK_APP=run.py
set FLASK_ENV=development
flask run &
start chrome --app=http://localhost:5000