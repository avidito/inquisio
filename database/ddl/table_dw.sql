-- News Count
DROP TABLE IF EXISTS dw.news_cnt;

CREATE TABLE dw.news_cnt(
  website VARCHAR,
  category VARCHAR,
  src_category VARCHAR,
  day DATE,
  cnt INT,
  load_dt TIMESTAMP
);

-- Top Tags
DROP TABLE IF EXISTS dw.top_tags;

CREATE TABLE dw.top_tags(
  website VARCHAR,
  tags VARCHAR,
  day DATE,
  cnt INT,
  load_dt TIMESTAMP
);