# all the imports!
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import model
import requests
import datetime

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
    url_template = "http://api.justin.tv/api/channel/embed/%s?volume=50"
    jtv_login = event.video_url
    r = requests.get(url_template%jtv_login)
   
    return render_template("event_view.html", event=event, 
    	embed_code=r.text)

@app.route("/event/edit/<int:id>")
def edit(id):
    event = g.db.query(model.Event).get(id)
    
    return render_template("event_edit.html", event=event)

@app.route("/event/save", methods=["POST"])
def save():
    if request.form["id"]:
        evt_id = int(request.form["id"])
        event = g.db.query(model.Event).get(evt_id)
    else:
        event = model.Event("","",datetime.datetime.utcnow(),"")
        g.db.add(event)
    event.title = request.form["title"] or event.title
    #event.happens_on = request.form["date"] 
    event.message = request.form["message"] or event.message
    event.video_url = request.form["channel"] or event.video_url
    g.db.commit()
    g.db.refresh(event)
    return redirect(url_for("view", id=event.id))

@app.route("/event/new")
def new():
    event = model.Event("","",datetime.datetime.utcnow(),"")
    return render_template("event_edit.html", event=event)   

# End Views

if __name__ == '__main__':
    app.run(host="0.0.0.0")


