import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey

Base = declarative_base()

db = None

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password 

    def __repr__(self):
        return "<User(%s, %s, %s)>"%(self.name, self.email, self.password)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    video_url =  Column(String)
    happens_on = Column(DateTime)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="events")

    def __init__(self, title, video_url, happens_on, message):
        self.title = title 
        self.video_url = video_url
        self.happens_on = happens_on
        self.message = message

"""
def fetch_user_by_email(email):
    results = db.execute("select id, name, email, password from users where email=%s"%email)
    result = results[0]
    u = User(id=result[0], name=result[1], email=result[2], password=result[3])

    event_results = db.execute("select id, title, video_url, happens_on, message where user_id=%d"%u.id)
    for event in event_results:
        evt = Event(event[0], event[1], event[2], event[3])
        evt.user = u
        u.events.append(evt)

    return u

#janine.events.append(Event("My totally awesome party", "http://...", datetime.datetime.utcnow(), "PLEASE ATTEND MY LAST MINUTE EVENT"))
"""

def connect():
    engine = create_engine("sqlite:////tmp/brideo.db")
    Session = sessionmaker(bind=engine)

    global db
    db = Session()


if __name__ == "__main__":
    connect()
