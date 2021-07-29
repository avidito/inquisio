-- Clear DW table
TRUNCATE dw.tags_cnt;

-- Insert data from query
INSERT INTO dw.tags_cnt
SELECT
  N.website AS website,
  T.tag AS tag,
  N.post_dt::DATE AS day,
  COUNT(*) AS cnt,
  CURRENT_TIMESTAMP AS load_dt
FROM src.tags T
LEFT JOIN src.map_news_tags MNT
  ON T.tag_id = MNT.tag_id
LEFT JOIN src.news N
  ON N.news_id = MNT.news_id
GROUP BY 1, 2, 3, 5;
