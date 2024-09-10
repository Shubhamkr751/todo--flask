from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)  
    done = db.Column(db.Boolean, default=False)    

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    if name: 
        new_task = Todo(name=name)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:task_id>') 
def update(task_id):
    todo = Todo.query.get(task_id)
    if todo:  
        todo.done = not todo.done
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete/<int:task_id>') 
def delete(task_id):
    todo = Todo.query.get(task_id)
    if todo:  
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
