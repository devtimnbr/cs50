-- SQL query to list the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred.
-- Your query should output a table with a single column for the title of each movie.
-- You may assume that there is only one person in the database with the name Bradley Cooper.
-- You may assume that there is only one person in the database with the name Jennifer Lawrence.
SELECT movies.title FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE people.name = "Johnny Depp" AND movies.title IN(
SELECT movies.title FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE people.name = "Helena Bonham Carter")