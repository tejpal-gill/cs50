SELECT DISTINCT(name) from people WHERE id IN
(SELECT person_id from stars WHERE movie_id IN
(SELECT id FROM movies WHERE year = 2004))
ORDER BY birth;