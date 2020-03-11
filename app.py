from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


db.create_all()


@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    tasks_amount = Task.query.count()
    issues = Issue.query.all()
    issues_amount = Issue.query.count()
    return render_template('list.html', tasks=tasks, issues=issues,
                                        tasks_amount=tasks_amount,
                                        issues_amount=issues_amount)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')


@app.route('/issue', methods=['POST'])
def add_issue():
    content = request.form['content']
    if not content:
        return 'Error'

    issue = Issue(content)
    db.session.add(issue)
    db.session.commit()
    return redirect('/')


@app.route('/task_delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/task_done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')


@app.route('/issue_delete/<int:issue_id>')
def delete_issue(issue_id):
    issue = Issue.query.get(issue_id)
    if not issue:
        return redirect('/')

    db.session.delete(issue)
    db.session.commit()
    return redirect('/')


@app.route('/issue_done/<int:issue_id>')
def resolve_issue(issue_id):
    issue = Issue.query.get(issue_id)

    if not issue:
        return redirect('/')
    if issue.done:
        issue.done = False
    else:
        issue.done = True

    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
