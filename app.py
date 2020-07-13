#Importing a few functions from flask to better my application
from flask import Flask, render_template, request, redirect, url_for, jsonify
#Importing SQLALCHEMY for all our db.X.X commands and X.query.X 
from flask_sqlalchemy import SQLAlchemy

import sys

from flask_migrate import Migrate

#set app equal to the filename! app.py is app
app = Flask(__name__)

#connecting to my database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:peaches777@127.0.0.1:5432/todoapp'
#eliminates the warning everytime you run flask run
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#in a way initializing SQLALCHEMY in my application allowing for db.session commands ro be run
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#class/model for Todo table
class Todo(db.Model):
	__tablename__ = 'todos'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(), nullable=False)
	completed = db.Column(db.Boolean, nullable=False, default=False)
	important = db.Column(db.Boolean, nullable=False, default=True)

	def __repr__(self):
		return f'<Todo {self.id} {self.description}>'
#using SQLALCHEMY I create Todo model with below function 
#db.create_all()

#setting the default route names index and using Flasks render_template to view HTML on teh client side
#also note the data attribute and how its using SQLALCHEMY to query.all() = select * from Todo;
@app.route('/')
def index():
	return render_template('index.html', data=Todo.query.order_by('id').all())

#setting a route for the creation of our Todo
#notice the route name.. this is nomenclature for this type of application
@app.route('/todos/create', methods=['POST'])
def create_todo():
	error = False
	body = {}
	try:
		description = request.get_json()['description']
		todo = Todo(description = description)
		db.session.add(todo)
		db.session.commit()
		body['description'] = todo.description
	except:
		error = True
		db.session.rollback()
		print(sys.exc_info())
	finally:
		db.session.close()
	if not error:
		return jsonify(body)



@app.route('/todos/<todo_id>set-completed', methods=['POST'])
def set_completed_todo(todo_id):
	try:
		completed = request.get_json()['completed']
		todo = Todo.query.get(todo_id)
		todo.completed = completed
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()
	return redirect(url_for('index'))
		

