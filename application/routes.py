from application import app, db
from application.models import Tasks
from application.forms import TaskForm
from flask import render_template, request, redirect, url_for

@app.route("/tasks/home")
@app.route("/tasks/")
@app.route("/")
def home():
    all_tasks = Tasks.query.all()
    return render_template("index.html", title="Home Page", all_tasks=all_tasks)

@app.route("/tasks/add", methods=["GET", "POST"])
def add():
    form = TaskForm()

    if request.method == "POST":
        new_task = Tasks(name=form.name.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("create_task.html", title="Add new Task", form=form)

@app.route("/tasks/showall")
def read():
    all_tasks = Tasks.query.all()
    tasks_dictionaty = {"tasks": []}
    for tasks in all_tasks:
        tasks_dictionaty["tasks"].append(
            {
                "Task": tasks.name,
                "Completed": tasks.completed
            }
        )
    return tasks_dictionaty

@app.route("/tasks/total")
def total_tasks():
    all_tasks = Tasks.query.all()
    return f"You have total of {len(all_tasks)} tasks to do."

@app.route("/tasks/update/<int:id>", methods=['GET', 'POST'])
def update_task(id):

    form = TaskForm()

    task = Tasks.query.get(id)

    if request.method == "POST":
        task.name = form.name.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("update_task.html", task=task, form=form)

@app.route("/tasks/delete/<int:id>")
def delete(id):
    tasks = Tasks.query.get(id)
    db.session.delete(tasks)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/tasks/completed/<int:id>')
def completed_task(id):
    task = Tasks.query.get(id)
    task.completed = True
    db.session.commit()
    return f"Task {id} has been completed"

@app.route('/tasks/incompleted/<int:id>')
def incomplete_task(id):
    task = Tasks.query.get(id)
    task.completed = False
    db.session.commit()
    return f"Task {id} is still not completed"