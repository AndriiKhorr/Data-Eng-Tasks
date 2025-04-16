-- ===============================================================
-- Тест для завдання 1: Кількість фільмів в кожній категорії
-- ===============================================================
-- Створення тимчасових таблиць
CREATE TEMP TABLE category (category_id INT, name TEXT);
CREATE TEMP TABLE film (film_id INT, title TEXT);
CREATE TEMP TABLE film_category (film_id INT, category_id INT);

-- Додавання тестових даних
INSERT INTO category VALUES (1, 'Action'), (2, 'Comedy');
INSERT INTO film VALUES (1, 'Movie A'), (2, 'Movie B');
INSERT INTO film_category VALUES (1, 1), (2, 1), (2, 2);

-- Очікування:
-- Action => 2 фільми (Movie A + Movie B)
-- Comedy => 1 фільм (Movie B)
SELECT c.name AS category, COUNT(f.film_id) AS film_count
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
GROUP BY c.name
ORDER BY film_count DESC;


-- ===============================================================
-- Тест для завдання 2: ТОП-10 акторів за кількістю прокатів
-- ===============================================================
CREATE TEMP TABLE actor (actor_id INT, first_name TEXT, last_name TEXT);
CREATE TEMP TABLE film_actor (actor_id INT, film_id INT);
CREATE TEMP TABLE inventory (inventory_id INT, film_id INT);
CREATE TEMP TABLE rental (rental_id INT, inventory_id INT);

INSERT INTO actor VALUES (1, 'Tom', 'Cruise');
INSERT INTO film_actor VALUES (1, 1);
INSERT INTO inventory VALUES (1, 1);
INSERT INTO rental VALUES (10, 1), (11, 1);

-- 🔍 Очікування:
-- Tom Cruise => 2 прокати
SELECT a.first_name || ' ' || a.last_name AS actor_name, COUNT(r.rental_id) AS rental_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN inventory i ON fa.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY actor_name
ORDER BY rental_count DESC
LIMIT 10;


-- ===============================================================
-- Тест для завдання 3: Категорія з найбільшими доходами
-- ===============================================================
CREATE TEMP TABLE payment (payment_id INT, rental_id INT, amount NUMERIC);
CREATE TEMP TABLE category (category_id INT, name TEXT);
CREATE TEMP TABLE film_category (film_id INT, category_id INT);
CREATE TEMP TABLE inventory (inventory_id INT, film_id INT);
CREATE TEMP TABLE rental (rental_id INT, inventory_id INT);

INSERT INTO category VALUES (1, 'Drama'), (2, 'Horror');
INSERT INTO film_category VALUES (1, 1), (2, 2);
INSERT INTO inventory VALUES (1, 1), (2, 2);
INSERT INTO rental VALUES (1, 1), (2, 2);
INSERT INTO payment VALUES (100, 1, 5.00), (101, 2, 3.00);

-- Очікування:
-- Drama => 5.00, Horror => 3.00 => Поверне Drama
SELECT c.name AS category, SUM(p.amount) AS total_revenue
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN inventory i ON fc.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.name
ORDER BY total_revenue DESC
LIMIT 1;


-- ===============================================================
-- Тест для завдання 4: Фільми, яких нема в inventory (без IN)
-- ===============================================================
CREATE TEMP TABLE film (film_id INT, title TEXT);
CREATE TEMP TABLE inventory (inventory_id INT, film_id INT);

INSERT INTO film VALUES (1, 'Alpha'), (2, 'Beta');
INSERT INTO inventory VALUES (1, 1);

-- Очікування:
-- 'Beta' не в inventory → має бути в результаті
SELECT f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.film_id IS NULL;


-- ===============================================================
-- Тест для завдання 5: Топ-3 актори у категорії “Children”
-- ===============================================================
CREATE TEMP TABLE actor (actor_id INT, first_name TEXT, last_name TEXT);
CREATE TEMP TABLE film_actor (actor_id INT, film_id INT);
CREATE TEMP TABLE film_category (film_id INT, category_id INT);
CREATE TEMP TABLE category (category_id INT, name TEXT);

INSERT INTO actor VALUES (1, 'Will', 'Smith');
INSERT INTO film_actor VALUES (1, 1), (1, 2);
INSERT INTO film_category VALUES (1, 1), (2, 1);
INSERT INTO category VALUES (1, 'Children');

--Очікування:
-- Will Smith => 2 фільми → має потрапити в топ
SELECT a.first_name || ' ' || a.last_name AS actor_name, COUNT(*) AS film_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN film_category fc ON fa.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
WHERE c.name = 'Children'
GROUP BY actor_name
ORDER BY film_count DESC
LIMIT 3;
