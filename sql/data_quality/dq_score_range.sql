SELECT CASE WHEN MIN(sentiment_score) >= -1
             AND MAX(sentiment_score) <= 1
           THEN 1 ELSE 0 END AS ok
FROM sentiment_analysis;
