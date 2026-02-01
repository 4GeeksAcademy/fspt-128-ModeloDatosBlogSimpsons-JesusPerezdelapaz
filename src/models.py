from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites_character_table = Table(
    "favorites_character",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
    
)

favorites_location_table = Table(
    "favorites_location",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorites_characters: Mapped["Character"] = relationship(
        "Character",
        secondary=favorites_character_table,
        back_populates="favorited_by"
    )
    favorites_locations: Mapped["Location"] = relationship(
        "Location",
        secondary=favorites_location_table,
        back_populates="favorited_by"
    )


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
        }
    

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    img: Mapped[str] = mapped_column(String(500), nullable=True)
    quote: Mapped[str] = mapped_column(String(500), nullable=True)
    favorited_by: Mapped[list[User]] = relationship(
        "User",
        secondary=favorites_character_table,
        back_populates="favorites_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "img": self.img
        }


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    img: Mapped[str] = mapped_column(String(500), nullable=True)
    use: Mapped[str] = mapped_column(String(200), nullable=True)
    town: Mapped[str] = mapped_column(String(200), nullable=True)
    favorited_by: Mapped[list[User]] = relationship(
        "User",
        secondary=favorites_location_table,
        back_populates="favorites_locations"
    )


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "use": self.use,
            "town": self.town,
            "img": self.img
        }