from datetime import datetime
from flask import render_template,session, redirect, url_for, current_app
from flask import request, flash
from flask_login import current_user
from . import main
from .. import db
from ..models import User, Post

@main.route('/', methods=['GET', 'POST'])
def index():
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PSGE'],
        error_out=True
        )
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/editpost', methods=['GET', 'POST'])
def editpost():
    if request.method == 'POST':
        post_data = request.form.to_dict()
        post = Post(**post_data)
        post.author = current_user._get_current_object()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('blog_edit.html')

@main.route('/post/<id>')
def post(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        return render_template('post.html', post=post)
    flash("i don't have this post,please visit other post")
    return redirect(url_for('main.index'))