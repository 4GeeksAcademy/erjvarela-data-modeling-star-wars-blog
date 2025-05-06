from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    favorite = relationship("Favorite", backref="user")


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), nullable=True)
    user = relationship("User", backref="favorites")
    planet = relationship("Planet", backref="favorites")
    people = relationship("People", backref="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    height: Mapped[float] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    mass: Mapped[float] = mapped_column(nullable=True)
    homeworld: Mapped[str] = mapped_column(String(120), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)
    favorite = relationship("Favorite", backref="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "homeworld": self.homeworld,
            "birth_year": self.birth_year,
            "url": self.url,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    surface_water: Mapped[float] = mapped_column(nullable=False)
    diameter: Mapped[float] = mapped_column(nullable=False)
    rotation_period: Mapped[float] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    gravity: Mapped[float] = mapped_column(nullable=False)
    orbital_period: Mapped[float] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    favorite = relationship("Favorite", backref="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "url": self.url,
            "description": self.description,
        }
