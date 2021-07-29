-- News
DROP TABLE IF EXISTS src.news;

CREATE TABLE src.news(
  news_id INT,
  category_id INT,
  content_id INT,
  title VARCHAR,
  website VARCHAR,
  url VARCHAR,
  author VARCHAR,
  post_dt TIMESTAMP,
  load_dt TIMESTAMP
);

-- Categories
DROP TABLE IF EXISTS src.categories;

CREATE TABLE src.categories(
  category_id INT,
  category VARCHAR,
  src_category VARCHAR,
  source VARCHAR,
  channel VARCHAR,
  update_dt TIMESTAMP
);

-- Contents
DROP TABLE IF EXISTS src.contents;

CREATE TABLE src.contents(
  partition_id INT,
  news_id INT,
  length INT,
  partition TEXT,
  load_dt TIMESTAMP
);

-- Tags
DROP TABLE IF EXISTS src.tags;

CREATE TABLE src.tags(
  tag_id INT,
  tag VARCHAR,
  source VARCHAR,
  channel VARCHAR,
  update_dt TIMESTAMP
);

-- Map News Tags
DROP TABLE IF EXISTS src.map_news_tags;

CREATE TABLE src.map_news_tags(
  news_id INT,
  tag_id INT
);
