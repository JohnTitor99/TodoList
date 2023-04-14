from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username", "class": "form-field"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "form-field"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username", "class": "form-field"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "form-field"})
    submit = SubmitField("Login")


class AddForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"class": "form-field"})
    description = TextAreaField(validators=[Length(min=0, max=300)], render_kw={"class": "add-des-field"})
    submit = SubmitField("Submit")