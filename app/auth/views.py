from . import auth
from flask import render_template,redirect,url_for
from flask import request,flash,make_response
from ..models import User, Comment
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
import re
import json

#访问前拦截器 防止恶意访问一些特殊页面
@auth.before_app_request
def before_requesg():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.admin and (request.endpoint in ['main.editpost','main.modifypost','main.deletepost']):
            print(request.endpoint in ['main.editpost','main.modifypost','main.deletepost'])
            flash('你没有访问的权限!')
            return redirect(url_for('main.index'))

#登录页面
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

#注销页面
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

#ajax验证用户名和email是否重复
@auth.route('/validate', methods=['GET', 'POST'])
def validate():
    if(request.args.get('username')):
        if User.query.filter_by(username=request.args.get('username')).first() is not None:
            return json.dumps([True])
    elif(request.args.get('email')):
        if User.query.filter_by(email=request.args.get('email')).first() is not None:
            return json.dumps([True])
    return json.dumps([False])

#注册页面
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
