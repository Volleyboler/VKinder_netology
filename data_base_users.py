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

# db = 'postgresql://{}:{}@localhost:5432/VKinter'.format(os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))
# engine = create_engine(db)


def create_database():
    create_db()


class VKUser(Base):
    __tablename__ = 'vk_user'
    vk_id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(80), nullable=False)
    last_name = sa.Column(sa.String(80))
    user_age = sa.Column(sa.Integer)
    range_for_search_age = sa.Column(sa.String(20))
    sex = sa.Column(sa.String(20))
    city = sa.Column(sa.String(60))


class DatingUser(Base):
    __tablename__ = 'dating_user'
    vk_id = sa.Column(sa.Integer, primary_key=True)
    dating_user_first_name = sa.Column(sa.String(80), nullable=False)
    dating_user_last_name = sa.Column(sa.String(80))
    age = sa.Column(sa.Integer)
    city = sa.Column(sa.String(20))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('vk_user.vk_id'))


class Photos(Base):
    __tablename__ = 'photos'
    photo_link = sa.Column(sa.String, primary_key=True)
    likes = sa.Column(sa.Integer)
    vk_id_dating_user = sa.Column(sa.Integer, sa.ForeignKey('dating_user.vk_id'))


class BlackList(Base):
    __tablename__ = 'blacklist'
    vk_id = sa.Column(sa.Integer, primary_key=True)
    dating_user_first_name = sa.Column(sa.String(80), nullable=False)
    dating_user_last_name = sa.Column(sa.String(80))
    age = sa.Column(sa.Integer)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('vk_user.vk_id'))
    city = sa.Column(sa.String(20))


Base.metadata.create_all(engine)


data_base_of_good_results = {}
data_base_of_black_list = {}
