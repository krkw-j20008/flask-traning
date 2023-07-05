from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT id, gender, body, birthday,edu,name,income'
        ' FROM marriage'
    ).fetchall()
    print('ok', posts)
    return render_template('main/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birthday = request.form['birthday']
        edu = request.form['edu']
        height = request.form['height']
        figure = request.form['figure']
        income = request.form['income']
        hobby = request.form['hobby']
        smoking = request.form['smoking']
        body = request.form['body']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO marriage (name, gender, birthday, edu,height,figure,income,hobby,smoking,body)'
                ' VALUES (?, ?, ?,?,?,?,?,?,?,?)',
                (name,gender,birthday,edu,height,figure,income,hobby,smoking,body)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT id,name, gender, birthday, edu,height,figure,income,hobby,smoking,body'
        ' FROM marriage '
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
        
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birthday = request.form['birthday']
        edu = request.form['edu']
        height = request.form['height']
        figure = request.form['figure']
        income = request.form['income']
        hobby = request.form['hobby']
        smoking = request.form['smoking']
        body = request.form['body']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)      
        else:
            db = get_db()
            db.execute(
                'UPDATE marriage SET name=?, gender=?,birthday=?,edu=?,height=?,figure=?,income=?,hobby=?,smoking=?,body=?'
                ' WHERE id = ?',
                (name,gender,birthday,edu,height,figure,income,hobby,smoking, body, id)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/update.html', post=post)