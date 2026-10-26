-- Requête 1 : combien d'hôtels dans la base ?
SELECT COUNT(*) AS nombre_hotels
FROM destinations_hotels;

-- Requête 2 : combien d'hôtels par ville ?
SELECT city, COUNT(*) AS nombre_hotels
FROM destinations_hotels
GROUP BY city
ORDER BY city;

-- Requête 3 : combien d'hôtels ont une note, et combien n'en ont pas ?
SELECT city,
       COUNT(*) AS nombre_hotels,
       COUNT(hotel_score) AS avec_note,
       COUNT(*) - COUNT(hotel_score) AS sans_note
FROM destinations_hotels
GROUP BY city
ORDER BY city;

-- Requête 4 : note moyenne des hôtels par ville (les hôtels sans note sont ignorés)
SELECT city, ROUND(AVG(hotel_score)::numeric, 2) AS note_moyenne
FROM destinations_hotels
GROUP BY city
ORDER BY note_moyenne DESC;

-- Requête 5 : les 10 meilleurs hôtels notés
SELECT LEFT(name, 32) AS hotel, city, hotel_score
FROM destinations_hotels
WHERE hotel_score IS NOT NULL
ORDER BY hotel_score DESC
LIMIT 10;
