# Import necessary modules
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import models as db_handler

# Create a Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.authenticated = False

    def is_authenticated(self):
        return self.authenticated


test_user = User('email', 'password')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    # open the connection to db
    conn = get_db_connection()
    # select the post base on it's id
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    # clos the connection
    conn.close()
    # checking if we already have the post or not
    if post is None:
        abort(404)
    return post


# Define a view function for the main route '/'
@app.route('/login', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def login():
    print(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = db_handler.retrieve_users()
        for user in users:
            if username == user[0] and password == user[1]:
                test_user.username = username
                test_user.password = password
                test_user.authenticated = True
                return redirect(url_for('home'))
        if 'register' in request.form:
            db_handler.insert_user(username, password)
    return render_template('login.html')


@app.route('/home')
def home():
    if not test_user.is_authenticated():
        return redirect(url_for('login'))
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    if not test_user.is_authenticated():
        return redirect(url_for('login'))

    # we got the post the user clicked on through the function we wrote before,
    # we save the value of the post in post variable
    post = get_post(post_id)
    # we render the post page, pass the post variable as an argument,
    # why? to be able to use it in the html page
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if not test_user.is_authenticated():
        return redirect(url_for('login'))

    # if the user clicked on Submit, it sends post request
    if request.method == 'POST':
        # Get the title and save it in a variable
        title = request.form['title']
        # Get the content the user wrote and save it in a variable
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            # Open a connection to database
            conn = get_db_connection()
            # Insert the new values in the db
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            # Redirect the user to index page
            return redirect(url_for('home'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if not test_user.is_authenticated():
        return redirect(url_for('login'))
    # Get the post to be edited by its id
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            # Update the table
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    if not test_user.is_authenticated():
        return redirect(url_for('login'))
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('home'))


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="127.0.0.1", debug=True)
