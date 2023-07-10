from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask import request
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    keyword = request.args.get('keyword', '')  # クエリパラメータからキーワードを取得
    gender = request.args.get('gender', '')  # クエリパラメータから性別を取得
    db = get_db()
    query = (
        'SELECT id, gender, body, birthday, name, income ,state,image'
        ' FROM marriage'
        ' WHERE name LIKE ?'  # キーワードに一致する名前のみを取得
    )
    params = ['%' + keyword + '%']
    if gender:  # 性別が選択されている場合はクエリに性別条件を追加
        query += ' AND gender = ?'
        params.append(gender)
    posts = db.execute(query, params).fetchall()
    
    return render_template('main/index.html', posts=posts)



    # db = get_db()
    # posts = db.execute(
    #     'SELECT id, gender, body, birthday,edu,name,income'
    #     ' FROM marriage'
    # ).fetchall()
    # return render_template('main/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birthday = request.form['birthday']
        edu = request.form['edu']
        
        work = request.form['work']
        
        height = request.form['height']
        figure = request.form['figure']
        income = request.form['income']
        hobby = request.form['hobby']
        smoking = request.form['smoking']
        body = request.form['body']
        state = request.form['state']

        f  = request.files['image']
        f.save(os.path.join('./flaskr/static/image-folder', f.filename))
        f = os.path.join('./static/image-folder', f.filename)

        error = None
  
        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO marriage (name, gender, birthday, edu,work,height,figure,income,hobby,smoking,body,state,image)'
                ' VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?)',
                (name,gender,birthday,edu,work,height,figure,income,hobby,smoking,body,state,f)
            )
            db.commit()

            return redirect(url_for('main.index'))
        


    return render_template('main/create.html', enctype='multipart/form-data')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT id,name, gender, birthday, edu,work,height,figure,income,hobby,smoking,body,state,image'
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
        work = request.form['work']
        height = request.form['height']
        figure = request.form['figure']
        income = request.form['income']
        hobby = request.form['hobby']
        smoking = request.form['smoking']
        body = request.form['body']
        state = request.form['state']
#        image = request.form['image']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)      
        else:
            db = get_db()
            db.execute(
                'UPDATE marriage SET name=?, gender=?,birthday=?,edu=?,work = ?,height=?,figure=?,income=?,hobby=?,smoking=?,body=?,state=?'
                ' WHERE id = ?',
                (name,gender,birthday,edu,work,height,figure,income,hobby,smoking, body,state, id)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/update.html', post=post)

# @bp.route('/<int:id>/view', methods=('GET', 'POST'))
# @login_required
# def view(id):

#     db = get_db()
#     db.execute(
#         'SELECT * from marriage '
#     )
    
