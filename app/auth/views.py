from . import auth
from flask import render_template,redirect,url_for
from flask import request,flash,make_response
from ..models import User, Comment
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
import re
import json

@auth.before_app_request
def before_requesg():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.admin and (request.endpoint == 'main.editpost' or request.endpoint == 'main.modifypost'):
            flash('你没有访问的权限!')
            return redirect(url_for('main.index'))

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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_data = request.form.to_dict()
        if login_data['email']!='' and login_data['username']!='' and  \
                                login_data['password']!='' and not User.validate_email(login_data['email']) and \
                                not User.validate_username(login_data['username']) and login_data['password']==login_data['password2'] and \
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
