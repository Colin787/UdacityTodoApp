#Importing a few functions from flask to better my application
from flask import Flask, render_template, request, redirect, url_for
#Importing SQLALCHEMY for all our db.X.X commands and X.query.X 
from flask_sqlalchemy import SQLAlchemy

#set app equal to the filename! app.py is app
app = Flask(__name__)

#connecting to my database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:peaches777@127.0.0.1:5432/todoapp'
#eliminates the warning everytime you run flask run
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#in a way initializing SQLALCHEMY in my application allowing for db.session commands ro be run
db = SQLAlchemy(app)

#class/model for Todo table
class Todo(db.Model):
	__tablename__ = 'todos'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(), nullable=False)

	def __repr__(self):
		return f'<Todo {self.id} {self.description}>'
#using SQLALCHEMY I create Todo model with below function 
db.create_all()

#setting the default route names index and using Flasks render_template to view HTML on teh client side
#also note the data attribute and how its using SQLALCHEMY to query.all() = select * from Todo;
@app.route('/')
def index():
	return render_template('index.html', data=Todo.query.all())

#setting a route for the creation of our Todo
#notice the route name.. this is nomenclature for this type of application
@app.route('/todos/create', methods=['POST'])
def create_todo():
	description = request.form.get('description', '')
	todo = Todo(description = description)
	db.session.add(todo)
	db.session.commit()
	return redirect(url_for('index'))