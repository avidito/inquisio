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

-- Tag Count
DROP TABLE IF EXISTS dw.tags_cnt;

CREATE TABLE dw.tags_cnt(
  website VARCHAR,
  tags VARCHAR,
  day DATE,
  cnt INT,
  load_dt TIMESTAMP
);
