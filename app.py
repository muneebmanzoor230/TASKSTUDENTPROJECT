from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

TASK_FILE = 'tasks.json'


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, 'r') as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


@app.route('/')
def home():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')

    tasks = load_tasks()

    tasks.append({
        'task': task,
        'completed': False
    })

    save_tasks(tasks)

    return redirect('/')


@app.route('/complete/<int:index>')
def complete_task(index):
    tasks = load_tasks()

    tasks[index]['completed'] = True

    save_tasks(tasks)

    return redirect('/')


@app.route('/delete/<int:index>')
def delete_task(index):
    tasks = load_tasks()

    tasks.pop(index)

    save_tasks(tasks)

    return redirect('/')


@app.route('/api/tasks')
def api_tasks():
    return load_tasks()


if __name__ == '__main__':
    app.run(debug=True)