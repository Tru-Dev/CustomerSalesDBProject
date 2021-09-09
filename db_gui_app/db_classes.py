from datetime import date
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

    def __init__(self, *args, **kwargs) -> None:
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.address = kwargs["address"]
        self.city = kwargs["city"]
        self.state = kwargs["state"]
        self.zip = int(kwargs["zip"])
        self.email = kwargs["email"]
        self.phone = kwargs["phone"]

class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("max_grade >= min_grade"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    min_grade = Column(Integer, CheckConstraint("min_grade >= 0")) # 0 = PreK
    max_grade = Column(Integer, CheckConstraint("max_grade <= 12"))
    price = Column(Numeric(13, 2))

    sales = relationship("Sale", back_populates="product")

    def __init__(self, *args, **kwargs) -> None:
        self.name = kwargs["name"]
        self.min_grade = int(kwargs["min_grade"])
        self.max_grade = int(kwargs["max_grade"])
        self.price = float(kwargs["price"])

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date)
    paid = Column(Numeric(13, 2))

    customer = relationship("Customer", back_populates="purchases")
    product = relationship("Product", back_populates="sales")

    def __init__(self, *args, **kwargs) -> None:
        self.customer_id = kwargs["customer_id"]
        self.product_id = kwargs["product_id"]
        self.date = date.fromisoformat(kwargs["date"])
        self.paid = float(kwargs["paid"])
