#!/usr/bin/python3
"""
Defines the DBStorage class.
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DBStorage class for storing objects in a database"""

    __engine = None
    __session = None

    def __init__(self):
        """Creates an instance of DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB'),
                                              pool_pre_ping=True))

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the current database session for all objects"""
        classes = ["State", "City", "User"]  # Add more classes as needed
        objects = {}

        if cls:
            query = self.__session.query(eval(cls))
            for obj in query:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for c in classes:
                query = self.__session.query(eval(c))
                for obj in query:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session"""
        self.__session.close()

