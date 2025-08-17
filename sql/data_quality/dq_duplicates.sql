WITH d AS (
  SELECT post_id
  FROM sentiment_analysis
  GROUP BY post_id
  HAVING COUNT(*) > 1
)
SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END AS ok
FROM d;
