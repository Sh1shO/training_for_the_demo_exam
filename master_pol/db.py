from sqlalchemy import *
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/asd"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Partners(Base):
    __tablename__="partners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_partner = Column(String(3))
    partner = Column(String(255))
    director = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    ur_adres = Column(String(255))
    inn = Column(String(12))
    rating = Column(Integer)

class Product(Base):
    __tablename__="product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_product_id = Column(Integer, ForeignKey("product_type.id"))
    name = Column(String(255))
    articul = Column(String(7))
    min_price = Column(MONEY)
    material_type_id = Column(Integer, ForeignKey("material_type.id"))

    type = relationship("Product_type")
    material = relationship("Material_type")

class Material_type(Base):
    __tablename__="material_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255))
    percent_brak = Column(Float)

class Product_type(Base):
    __tablename__="product_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255))
    koef = Column(Float)

class Partner_product(Base):
    __tablename__="partner_product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_partner_id = Column(Integer, ForeignKey("partners.id"))
    count = Column(Integer)
    date = Column(Date)
    name_product_id = Column(Integer, ForeignKey("product.id"))

    partner = relationship("Partners")
    product = relationship("Product")

def get_session():
    return Session()

Base.metadata.create_all(engine)