import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'SearchResults.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)


def create_database():
    create_db()


class VKUser(Base):
    __tablename__ = 'vk_user'
    vk_id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(80), nullable=False)
    last_name = sa.Column(sa.String(80))
    user_age = sa.Column(sa.Integer)
    sex = sa.Column(sa.Integer)
    city = sa.Column(sa.String(60))
    city_id = sa.Column(sa.Integer)

    def __init__(self, vk_id: int, first_name: str, last_name: str, user_age: int, sex: int, city: dict):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_age = user_age
        self.sex = sex
        self.city = city['title']
        self.city_id = city['id']


class DatingUser(Base):
    __tablename__ = 'dating_user'
    vk_id = sa.Column(sa.Integer, primary_key=True)
    dating_user_first_name = sa.Column(sa.String(80), nullable=False)
    dating_user_last_name = sa.Column(sa.String(80))
    birthdate = sa.Column(sa.String(30))
    sex = sa.Column(sa.Integer)
    city = sa.Column(sa.String(30))
    city_id = sa.Column(sa.Integer)
    best_photos = sa.Column(sa.String(100))
    user_domain = sa.Column(sa.String(100))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('vk_user.vk_id'))

    def __init__(self, vk_id: int, dating_user_first_name: str, dating_user_last_name: str, birthdate: str, sex: int,
                 city: dict, best_photos: str, user_domain: str, user_id: int):
        self.vk_id = vk_id
        self.dating_user_first_name = dating_user_first_name
        self.dating_user_last_name = dating_user_last_name
        self.birthdate = birthdate
        self.sex = sex
        self.city = city['title']
        self.city_id = city['id']
        self.best_photos = best_photos
        self.user_domain = user_domain
        self.user_id = user_id


class BlackList(Base):
    __tablename__ = 'blacklist'
    vk_id = sa.Column(sa.Integer, primary_key=True)
    black_list_user_first_name = sa.Column(sa.String(80), nullable=False)
    black_list_user_last_name = sa.Column(sa.String(80))
    birthdate = sa.Column(sa.String(30))
    sex = sa.Column(sa.Integer)
    city = sa.Column(sa.String(30))
    city_id = sa.Column(sa.Integer)
    best_photos = sa.Column(sa.String(100))
    user_domain = sa.Column(sa.String(100))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('vk_user.vk_id'))

    def __init__(self, vk_id: int, black_list_user_first_name: str, black_list_user_last_name: str, birthdate: str,
                 sex: int, city: dict, best_photos: str, user_domain: str, user_id: int):
        self.vk_id = vk_id
        self.black_list_user_first_name = black_list_user_first_name
        self.black_list_user_last_name = black_list_user_last_name
        self.birthdate = birthdate
        self.sex = sex
        self.city = city['title']
        self.city_id = city['id']
        self.best_photos = best_photos
        self.user_domain = user_domain
        self.user_id = user_id


Base.metadata.create_all(engine)
