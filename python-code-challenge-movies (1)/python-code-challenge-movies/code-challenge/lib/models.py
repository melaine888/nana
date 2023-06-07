import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

engine = create_engine('sqlite:///db/movies.db', echo=True)
Session = sessionmaker(bind = engine)
session = Session()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    actor_id = Column(Integer, ForeignKey('actors.id'))
    salary = Column(Integer)
    character_name = Column(String)

    movie = relationship("Movie", back_populates="roles")
    actor = relationship("Actor", back_populates="roles")

    def actor(self):
        return self.actor

    def movie(self):
        return self.movie


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String())

    # movies = relationship("Movie", secondary="", back_populates="actor")

    roles = relationship("Role", back_populates="actor")

    def get_roles(self):
        return self.roles

    def get_movies(self):
        return [role.movie for role in self.roles]
    
    def total_salary(self):
        return sum(role.salary for role in self.roles)
    
    def blockbusters(self):
        return [role.movie for role in self.roles if role.movie.box_office_earnings > 50000000]
    
    @classmethod
    def most_successful(cls):
        actors = session.query(cls).all()
        return max(actors, key=lambda actor: actor.total_salary())

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    box_office_earnings = Column(Integer())

    roles = relationship("Role", back_populates="movie")

    # actors = relationship("Role", back_populates="movie")

    def get_roles(self):
        return self.roles

    def get_actors(self):
        return [role.actor for role in self.roles]
    
    def roles(self):
        return self.roles
    
    def actors(self):
        return [role.actor for role in self.roles]
    
    def cast_role(self, actor, character_name, salary):
        role = Role(actor=actor, movie=self, character_name=character_name, salary=salary)
        session.add(role)
        session.commit()

    def all_credits(self):
        return [f"{role.character_name}: Played by {role.actor.name}" for role in self.roles]
    
    def fire_actor(self, actor):
        role = session.query(Role).filter(Role.actor == actor, Role.movie == self).first()
        if role:
            session.delete(role)
            session.commit()

     
    

   
