from . import auth
from flask import render_template,redirect,url_for
from flask import request,flash,make_response
from ..models import User
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
import re
import json

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        print (user_data['email'])
        user = User.query.filter_by(email=user_data['email']).first()
        if user is not None and user.verify_password(user_data['password']):
            login_user(user, user_data.get('remember_me',False))
            print('登录成功',user_data['email'])
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的用户名或者密码.')
    return render_template('auth/login.html')

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/validate', methods=['GET', 'POST'])
def validate():
    if(request.args.get('username')):
        if User.query.filter_by(username=request.args.get('username')).first() is not None:
            return json.dumps([True])
    elif(request.args.get('email')):
        if User.query.filter_by(email=request.args.get('email')).first() is not None:
            return json.dumps([True])
    return json.dumps([False])

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_data = request.form.to_dict()
        if login_data['email']!='' and login_data['username']!='' and  \
                                login_data['password']!='' and not User.validate_email(login_data['email'] and \
                                not User.validate_username(login_data['username']) and login_data['password']!=login_data['password2']) and \
                             re.findall(r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)',login_data['email']):
            user = User(email=login_data['email'],
                    username=login_data['username'],
                    password=login_data['password'])
            db.session.add(user)
            db.session.commit()
            print('success {} register'.format(login_data['email']))
            flash('恭喜你，注册成功!')
            return redirect(url_for('auth.login'))
        flash('输入的数据有错误!')
    return render_template('auth/register.html') 