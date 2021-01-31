from flask import flash, session, url_for, request, make_response, redirect, render_template
from flask_bootstrap import Bootstrap
import unittest
from app import create_app
from  app.forms import LoginForm

app = create_app()

todos = ['comprar cafe','Enviar solucitud de compra','entregar video al productor']

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
def hello():
    user_ip = session.get('user_ip') #optener dato de la ip oculta por seguridad en sessions
    login_form = LoginForm()
    username = session.get('username')
    
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username':username
    }
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] =  username

        flash('Nombre de usuario registrado con exito')

        return redirect(url_for('index'))

    return render_template('hello.html', **context) #renderear un template
