from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileAllowed , FileField
from wtforms import StringField , EmailField , PasswordField ,SubmitField , BooleanField 
from wtforms.validators import DataRequired , Length , Email ,EqualTo , ValidationError
from Flask_app.models import User

class RegistrationForm(FlaskForm):
   username = StringField('Username',
                    validators=[DataRequired(),Length(min=2,max=20)])
   email = EmailField('Email',validators=[DataRequired(),Email()])
   password = PasswordField("Password",validators=[DataRequired()])
   confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password',message='Password must match')])
   submit = SubmitField('Sign Up')

   def validate_username(self,username):
       user = User.query.filter_by(username=username.data).first()
       if user:
          raise ValidationError("Username Already Exist")
   
   def validate_email(self,email):
      email = User.query.filter_by(email=email.data).first()
      if email:
         raise ValidationError("Email Already Exist")


#Login Form For the website
class LoginForm(FlaskForm):
   email = StringField('Email',validators=[DataRequired(),Email()])
   password = PasswordField("Password",validators=[DataRequired()])
   remember = BooleanField('Remember Me')
   submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
   username = StringField('Username',validators=[DataRequired(),Length(min=2,max=30)])
   email = StringField("Email",validators=[DataRequired(),Email()])
   submit = SubmitField("Update")
   picture = FileField("Update Profile Picture",validators=[FileAllowed(['png','jpg'])])

   def validate_username(self,username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
         raise ValidationError("That username Exist")
   
   def validate_email(self,email):
     if email.data != current_user.email:
      email = User.query.filter_by(email=email.data).first()
      if email:
         raise ValidationError("That email Exist")


class RequestResetForm(FlaskForm):
   email = EmailField('Email',validators=[DataRequired(),Email()])
   submit = SubmitField("Request Password Reset")

   def validate_email(self,email):
      user = User.query.filter_by(email=email.data).first()
      if user is None:
         raise ValidationError("No account with this email , you should Register")

class ResetPasswordForm(FlaskForm):
   password = PasswordField("Password",validators=[DataRequired()])
   confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
   submit = SubmitField('Reset Password')
