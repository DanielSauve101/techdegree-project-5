from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import forms
import models

DEBUG = True


app = Flask(__name__)
app.secret_key = 'asdfh4897*^jh390gkl20-asdklkl34098gj34589sdghrui^&%$'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


def get_entry(id):
    """Function to get model object based on id."""
    try:
        entry = models.Entry.select().where(models.Entry.id == id).get()
    except models.DoesNotExist:
        abort(404)
    return entry


@app.route('/register', methods=('GET', 'POST'))
def register():
    """View to show register form and validate data for a new user."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You have registered successfully!")
        models.User.create_user(
            username=form.username.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """View to have user login and validate credentials."""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("You're username or password does not match.")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are logged in!")
                return redirect(url_for('index'))
            else:
                flash("You're email or password does not match.")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """View that logs out the user."""
    logout_user()
    flash("You have been logged out successfully!")
    return redirect(url_for('index'))


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def new_entry():
    """View that shows the form to create a new entry and validates data."""
    form = forms.EntryForm()
    if form.validate_on_submit():
        flash("You have successfully added a new entry!")
        models.Entry.create(
            user=g.user._get_current_object(),
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<id>')
def view_entry(id):
    """View that shows the details of a selected entry."""
    entry = get_entry(id)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit_entry(id):
    """View that allows the user to edit there entry using a form."""
    existing_entry = get_entry(id)
    form = forms.EntryForm()
    if form.validate_on_submit():
        flash("You have successfully edited your entry!")
        update_entry = models.Entry.update(
            user=g.user._get_current_object(),
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            learned=form.learned.data,
            resources=form.resources.data
        ).where(models.Entry.id == id)
        update_entry.execute()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, entry=existing_entry)


@app.route('/entries/<id>/delete')
@login_required
def delete_entry(id):
    """View that allows the user to delete their entry."""
    delete_entry = get_entry(id)
    delete_entry.delete_instance()
    flash("You have successfully deleted the entry")
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
def index():
    """View that is the home page which shows a list of entries."""
    entries = models.Entry.select().order_by(models.Entry.date.desc())
    return render_template('index.html', entries=entries)


if __name__ == '__main__':
    models.initialise()
    app.run(debug=DEBUG)
