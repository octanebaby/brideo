# all the imports!
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import model

# configuration
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'

#create our app!

app = Flask (__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    model.connect()
    g.db = model.db

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route("/")
def home():
    events = g.db.query(model.Event).all()
    return render_template("home_page.html", events=events)

@app.route("/event/view/<int:id>")
def view(id):
    event = g.db.query(model.Event).get(id)
    return render_template("event_view.html", event=event)

# End Views

if __name__ == '__main__':
    app.run(host="0.0.0.0")


