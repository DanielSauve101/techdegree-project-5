from flask import (Flask, g, render_template, flash, redirect, url_for, abort)

import forms
import models

DEBUG = True


app = Flask(__name__)
app.secret_key = 'asdfh4897*^jh390gkl20-asdklkl34098gj34589sdghrui^&%$'


if __name__ = '__main__':
    models.initialise()
    app.run(debug=DEBUG)
