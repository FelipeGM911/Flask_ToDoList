from flask import flash, session, url_for, request, make_response, redirect, render_template
from flask_login import login_required, current_user

import unittest
from app import create_app
from  app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm

from app.firestore_service import get_users, get_todos, delete_todo , put_todo, update_todo

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)

#index o inio del proyecto
@app.route('/') #rutas de proyecto
def index():
    user_ip = request.remote_addr #optener ip de usuario

    response = make_response(redirect('/hello')) #redirecciona a hello
    session['user_ip'] = user_ip #ocultar ip en sessions

    return response


@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
    user_ip = session.get('user_ip') #optener dato de la ip oculta por seguridad en sessions
    username = current_user.id
    #Todo form
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username':username,
        'todo_form':todo_form,
        'delete_form':delete_form,
        'update_form':update_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)
        
        flash('Tarea agregada')
        
        return redirect(url_for('hello'))

    return render_template('hello.html', **context) #renderear un template


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))

