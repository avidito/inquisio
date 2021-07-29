from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text


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
	category = Column(String)
	src_category = Column(String)
	source = Column(String)
	channel = Column(String)
	update_dt = Column(DateTime)

class Contents(Base):
	__tablename__ = "contents"
	__table_args__ = {"schema": "src"}

	partition_id = Column(Integer, primary_key=True)
	news_id = Column(Integer, primary_key=True)
	length = Column(Integer)
	partition = Column(Text)
	load_dt = Column(DateTime)

class Tags(Base):
	__tablename__ = "tags"
	__table_args__ = {"schema": "src"}

	tag_id = Column(Integer, primary_key=True)
	tag = Column(String)
	source = Column(String)
	channel = Column(String)
	update_dt = Column(DateTime)

class MapNewsTags(Base):
	__tablename__ = "map_news_tags"
	__table_args__ = {"schema": "src"}

	news_id = Column(Integer, primary_key=True)
	tag_id = Column(Integer, primary_key=True)


TABLE_MODELS = {
	"news": News,
	"categories": Categories,
	"contents": Contents,
	"tags": Tags,
	"map_news_tags": MapNewsTags
}
