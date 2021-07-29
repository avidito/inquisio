-- Clear DW table
TRUNCATE dw.news_cnt;

-- Insert data from query
INSERT INTO dw.news_cnt
SELECT
  N.website AS website,
  C.gen_category AS category,
  C.src_category AS src_category,
  N.post_dt::DATE AS day,
  COUNT(*) AS cnt,
  CURRENT_TIMESTAMP AS load_dt
FROM src.categories C
LEFT JOIN src.news N
  ON C.category_id = N.category_id
GROUP BY 1, 2, 3, 4, 6;
