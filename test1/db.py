from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/kr2"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__="user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50))
    name = Column(String(50))
    patronymic = Column(String(50))
    group_id = Column(Integer, ForeignKey("group.id"))
    date = Column(Date)

    group = relationship("Group")

class Group(Base):
    __tablename__="group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

Base.metadata.create_all(engine)