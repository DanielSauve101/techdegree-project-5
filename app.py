from flask import (Flask, g, render_template, flash, redirect, url_for, abort)

import forms
import models

DEBUG = True


app = Flask(__name__)
app.secret_key = 'asdfh4897*^jh390gkl20-asdklkl34098gj34589sdghrui^&%$'


@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
    form = forms.NewEntryForm()
    if form.validate_on_submit():
        flash("You have successfully added a new entry!", "success")
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(25)
    return render_template('index.html', entries=entries)


if __name__ == '__main__':
    models.initialise()
    app.run(debug=DEBUG)
