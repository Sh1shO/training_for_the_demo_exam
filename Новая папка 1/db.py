from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/test"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

    
class Type_neispravnosti(Base):
    __tablename__="type_neispravnosti"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    
class Status(Base):
    __tablename__="status"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

class Type_oboryd(Base):
    __tablename__="type_oboryd"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    
class Employee(Base):
    __tablename__="employee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50))
    name = Column(String(50))
    patronymic = Column(String(50))
    
class Order(Base):
    __tablename__="order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    oboryd_id = Column(Integer, ForeignKey("type_oboryd.id"))
    type_neisprav_id = Column(Integer, ForeignKey("type_neispravnosti.id"))
    description = Column(String(255))
    last_name = Column(String(50))
    name = Column(String(50))
    patronymic = Column(String(50))
    status_id = Column(Integer, ForeignKey("status.id"))
    employee_id = Column(Integer, ForeignKey("employee.id"))
    
    oboryd = relationship("Type_oboryd")
    neisprav = relationship("Type_neispravnosti")
    status = relationship("Status")
    employee = relationship("Employee")

    
Base.metadata.create_all(engine)
    
