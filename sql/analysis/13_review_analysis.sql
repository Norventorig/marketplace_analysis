WITH orders_total AS(
	SELECT
		order_id,
		SUM(price) AS total
	FROM order_items
	GROUP BY order_id
)

SELECT
	review_score,
	ROUND(AVG(total), 2) AS avg_order,
	COUNT(*) AS reviews
FROM order_reviews AS r
JOIN orders_total USING(order_id)
GROUP BY review_score
ORDER BY review_score;

-- Анализирует связь между рейтингом отзыва и стоимостью заказа.
-- Показывает: оценку отзыва; среднюю стоимость заказа; количество отзывов.
