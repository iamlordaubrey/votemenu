from uuid import uuid4

from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String)
    location = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    restaurant_id = Column(UUID, ForeignKey('restaurant.id'))

    restaurant = relationship('Restaurant')


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    content = Column(JSON)
    restaurant_id = Column(UUID, ForeignKey('restaurant.id'))

    created_at = Column(DateTime(timezone=True), default=func.now())

    restaurant = relationship('Restaurant')


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    employee_id = Column(UUID, ForeignKey('employee.id'))
    menu_one_id = Column(UUID, nullable=True)
    menu_two_id = Column(UUID, nullable=True)
    menu_three_id = Column(UUID, nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now())

    employee = relationship('Employee')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
