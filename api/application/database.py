from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime

from application.utils import get_params

params = get_params()
username = params["USERNAME"]
password = params["PASSWORD"]
hostname = params["HOSTNAME"]
port = params["PORT"]
database = params["DATABASE"]

########## Engine ##########
def get_db():
    db_engine = create_engine(f"postgresql://{username}:{password}@{hostname}:{port}/{database}")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    return Session()

########## Models ##########
Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    __table_args__ = {"schema": "src"}

    news_id = Column(Integer, primary_key=True)
    category_id = Column(Integer)
    content_id = Column(Integer)
    title = Column(String)
    website = Column(String)
    url = Column(String)
    author = Column(String)
    post_dt = Column(DateTime)
    load_dt = Column(DateTime)

class Categories(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "src"}

    category_id = Column(Integer, primary_key=True)
    src_category = Column(String)
    gen_category = Column(String)
    source = Column(String)
    update_dt = Column(DateTime)

class Contents(Base):
    __tablename__ = "contents"
    __table_args__ = {"schema": "src"}

    partition_id = Column(Integer, primary_key=True)
    news_id = Column(Integer)
    length = Column(Integer)
    partition = Column(String)
    load_dt = Column(DateTime)

class Tags(Base):
    __tablename__ = "tags"
    __table_args__ = {"schema": "src"}

    tag_id = Column(Integer, primary_key=True)
    tag = Column(String)
    update_dt = Column(DateTime)

class MapNewsTags(Base):
    __tablename__ = "map_news_tags"
    __table_args__ = {"schema": "src"}

    news_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)
