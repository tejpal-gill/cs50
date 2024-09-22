SELECT name FROM people WHERE id IN
(SELECT DISTINCT(person_id) from directors WHERE movie_id IN
(SELECT movie_id FROM ratings WHERE rating >= 9.0))