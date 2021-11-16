from application import app, db
from application.models import Tasks

@app.route("/tasks/add/<name>")
def add(name):
    new_task = Tasks(name=name)
    db.session.add(new_task)
    db.session.commit()
    return f"Added {new_task.id} to the list"

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

@app.route("/tasks/update/<int:id>/<name>")
def update(id, name):
    tasks = Tasks.query.get(id)
    tasks.name = name
    db.session.commit()
    return f"Updated task {name} to new {tasks.name}"

@app.route("/tasks/delete/<int:id>")
def delete(id):
    tasks = Tasks.query.get(id)
    db.session.delete(tasks)
    db.session.commit()
    return f"Task {id} has been deleted"

@app.route('/tasks/completed/<int:id>')
def complete_task(id):
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