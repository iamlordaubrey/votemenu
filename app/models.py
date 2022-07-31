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