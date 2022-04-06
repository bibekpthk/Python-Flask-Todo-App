from email.policy import default
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_fontawesome import FontAwesome

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)
datepicker(app)
fa = FontAwesome(app)


class Todo(db.Model): #database model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    task_description =db.Column(db.String(), nullable = True)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_title = request.form["task"]
        task_due_date_string = request.form["dueDate"] #input date as string
        task_due_date = datetime.strptime(task_due_date_string, "%Y-%m-%d") #convert to date time and strip time
        task_description_string = request.form["task_description"]
        new_task = Todo(title=task_title, due_date=task_due_date, task_description=task_description_string )
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There is an issue"
    else:
        tasks = Todo.query.order_by(Todo.due_date).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return "There is a Problem while deleting todo item !!"


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.title = request.form["task"]
        task_due_date_string= request.form["dueDate"]
        task_due_date_string=task_due_date_string[:10] #since we are stripping time, only using YYYY-MM-DD as 10 characters
        task.due_date = datetime.strptime(task_due_date_string, "%Y-%m-%d") #converting string date to datetime
        task.task_description = request.form["task_description"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Oh snap I ran into an issue !!"
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()

        return render_template("index.html", update_task=task, tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)

