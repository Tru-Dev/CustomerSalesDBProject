from sqlalchemy import (
    create_engine, Column,
    Integer, String, Numeric, Date,
    ForeignKey, CheckConstraint
)
from sqlalchemy.orm import declarative_base, Session, relationship

from . import config

conn_str = config.config.connection
if config.config.relative:
    conn_str = config.MAIN_FOLDER / conn_str
conn_str = config.config.url_schema + str(conn_str)

engine = create_engine(conn_str)
session = Session(engine)

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    address = Column(String(50))
    city = Column(String(15))
    state = Column(String(15))
    zip = Column(Integer)
    email = Column(String(40))
    phone = Column(String(25))

    purchases = relationship("Sale", back_populates="customer")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("max_grade >= min_grade"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    max_grade = Column(Integer, CheckConstraint("max_grade <= 12"))
    min_grade = Column(Integer, CheckConstraint("min_grade >= 0")) # 0 = PreK
    price = Column(Numeric(13, 2))

    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date)
    paid = Column(Numeric(13, 2))

    customer = relationship("Customer", back_populates="purchases")
    product = relationship("Product", back_populates="sales")



