from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField #field de loginForm class
from wtforms.validators import DataRequired #Validador de datos

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class TodoForm(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired()])
    submit = SubmitField('Crear')