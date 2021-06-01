import os
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

db = SQLAlchemy()
'''
setup_db
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://adrianabarca@localhost:5432/movie_test'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Movie
    A movie object, extends the base SQLAlchemy model
'''
class Movie(db.Model):
  __tablename__ = 'Movie'
  id = Column(Integer, primary_key=True)
  title = Column(String(100), unique=True, nullable=False)
  release_date = Column(DateTime(), nullable=False)
  actors = relationship('Actor', backref='Movie', lazy=True)

  '''
  insert()
    inserts a new Movie model into a database
    model must have a title, release_date, and actors
    EXAMPLE
        actors = Actor.query.all()
        movie = Movie(title=new_title, release_date=new_release_date, actors=actors)
        movie.insert()
  '''
  def insert(self):
      db.session.add(self)
      db.session.commit()

  '''
  delete()
    deletes a Movie model from a database
    model must exist in the database
    EXAMPLE
        actors = Actor.query.all()
        movie = Movie(title=new_title, release_date=new_release_date, actors=actors)
        movie.delete()
  '''
  def delete(self):
      db.session.delete(self)
      db.session.commit()

  '''
    update()
        updates a new Movie model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Star Wars'
            movie.update()
    '''
  def update(self):
      db.session.commit()


'''
Actor
    an Actor object, extends the base SQLAlchemy model
'''
class Actor(db.Model):
  __tablename__ = 'Actor'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  age = Column(Integer)
  gender = Column(String(50), primary_key=True)
  movies_id = Column(Integer, db.ForeignKey('Movie.id', ondelete='CASCADE'))
  '''
  insert()
    inserts a new Actor model into a database
    model must have a name, an age, and a gender
    EXAMPLE
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.insert()
  '''
  def insert(self):
      db.session.add(self)
      db.session.commit()

  '''
  delete()
    deletes an Actor model from a database
    model must exist in the database
    EXAMPLE
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.delete()
  '''
  def delete(self):
      db.session.delete(self)
      db.session.commit()

  '''
    update()
        updates a new Actor model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Adrian'
            actor.update()
    '''
  def update(self):
      db.session.commit()
