from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), 
    Length(min=4,max=40)],render_kw={"placeholder":"Email"})
    username = StringField(validators=[InputRequired(), 
    Length(min=4, max=20)],render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), 
    Length(min=4,max=20)],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(),
    Length(min=4,max=20)],render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField("Register")

    def validate_username_email(self,username,email,User):
        existing_user = User.query.filter_by(username = username.data).first()
        existing_email = User.query.filter_by(email = email.data).first()
        if existing_user or existing_email:
            return False
        else:
            return True

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(),
    Length(min=4,max=40)], render_kw={"placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(),
    Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

class GameForm(FlaskForm):
    name = StringField(validators=[InputRequired(), 
    Length(min=4,max=40)], render_kw={"placeholder":"Name"})
    description = TextAreaField(render_kw={"placeholder":"Description"})
    submit = SubmitField("Create Game")
