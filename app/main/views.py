from datetime import datetime
from flask import render_template,session, redirect, url_for, current_app
from flask import request, flash
from flask_login import current_user, login_required
from . import main
from .. import db
from ..models import User, Post, Comment

#模版首页
@main.route('/', methods=['GET', 'POST'])
def index():
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PSGE'],
        error_out=True
        )
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)

#编辑文章页
@main.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    if request.method == 'POST':
        post_data = request.form.to_dict()
        post = Post(**post_data)
        post.author = current_user._get_current_object()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('blog_edit.html')

#修改文章页
@main.route('/modifypost/<int:id>', methods=['GET', 'POST'])
@login_required
def modifypost(id):
    if request.method == 'GET':
        post = Post.query.get_or_404(id)
        return render_template('blog_modify.html', post=post)
    else:
        post = Post.query.get_or_404(id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', id=id))

#浏览文章
@main.route('/post/<id>')
def post(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        comments = Comment.query.filter_by(post_id=id).all()
        return render_template('post.html', post=post, comments=comments)
    flash("i don't have this post,please visit other post")
    return redirect(url_for('main.index'))

#添加评论
@main.route('/addcomment/<int:id>', methods=['GET', 'POST'])
@login_required
def addcomment(id):
    post = Post.query.get_or_404(id)
    comment = Comment(post=post, user=current_user._get_current_object(),
                user_name=current_user.username, user_image=current_user.gravator(), content=request.form['content'])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('main.post', id=id))

#删除文章
@main.route('/deletepost/<int:id>')
@login_required
def deletepost(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    return redirect(url_for('main.index'))