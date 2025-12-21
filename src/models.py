from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites_char: Mapped[list['FavCharacters']] = relationship(back_populates='users_c')
    favorites_plan: Mapped[list['FavPlanets']] = relationship(back_populates='users_p')
    favorites_star: Mapped[list['FavStarships']] = relationship(back_populates='users_s')


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def __repr__(self):
        return f'{self.email}'
    

class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    weigth: Mapped[int] = mapped_column(Integer)
    favorites_by_char: Mapped[list['FavCharacters']] = relationship(back_populates='people')

    def __repr__(self):
        return f'{self.name}'

class FavCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users_c: Mapped['User'] = relationship(back_populates='favorites_char')
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    people: Mapped['Characters'] = relationship(back_populates='favorites_by_char')

class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer)
    orbital_period: Mapped[int] = mapped_column(Integer)
    favorites_by_plan: Mapped[list['FavPlanets']] = relationship(back_populates='astros')

    def __repr__(self):
        return f'{self.name}'

class FavPlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users_p: Mapped['User'] = relationship(back_populates='favorites_plan')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    astros: Mapped['Planets'] = relationship(back_populates='favorites_by_plan')

class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    passengers: Mapped[int] = mapped_column(Integer)
    cargo_capacity: Mapped[int] = mapped_column(Integer)
    favorites_by_star: Mapped[list['FavStarships']] = relationship(back_populates='naves')

    def __repr__(self):
        return f'{self.name}'

class FavStarships(db.Model):
    __tablename__ = 'favorite_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    users_s: Mapped['User'] = relationship(back_populates='favorites_star')
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    naves: Mapped['Starships'] = relationship(back_populates='favorites_by_star')