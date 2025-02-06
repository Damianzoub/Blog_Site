from flask import Blueprint , render_template , url_for , flash , redirect , request
from flask_login import current_user ,logout_user , login_user , login_required
from Flask_app.users.utils import save_picture , send_reset_email
from Flask_app.users.forms import LoginForm,RegistrationForm , RequestResetForm , UpdateAccountForm ,ResetPasswordForm
from Flask_app.models import User,Post


users = Blueprint('users',__name__) 

@users.route("/register",methods=['GET','POST'])
def register():
    from Flask_app import db,bcrypt

    if current_user.is_authenticated:
         return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email = form.email.data , password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash("Account was created",'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title="Register",form=form)

@users.route("/login",methods=["GET","POST"])
def login():
    from Flask_app import bcrypt

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccesful Please check email and password","danger")    
    return render_template("login.html",title="Login",form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    from Flask_app import db,bcrypt
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('account been updated','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',
                           image_file=image_file, form=form)




@users.route("/reset_password",methods=["GET","POST"])
def reset_request():
   if current_user.is_authenticated:
       return redirect(url_for('main.home'))
   form = RequestResetForm()
   if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       send_reset_email(user)
       flash('an email has been sent with instruction to reset password','info')
       return redirect(url_for('users.login'))
   return render_template('reset_request.html',title='Reset Password',form = form)

@users.route('/reset_password/<token>',methods=["GET","POST"])
def reset_token(token):
    from Flask_app import db,bcrypt
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
         flash('That is an invalid or expired token','warning')
         return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your account has been updated! You are now able to log in ','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)
