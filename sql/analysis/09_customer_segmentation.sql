WITH spending AS (
	SELECT
		customer_unique_id,
		SUM(price) AS total
	FROM customers AS c
	
	JOIN orders AS o USING(customer_id)
	JOIN order_items AS oi USING(order_id)
	
	GROUP BY customer_unique_id
)

SELECT
	customer_unique_id,
	total,

CASE

WHEN total < 100 THEN 'Low'
WHEN total < 500 THEN 'Medium'
WHEN total < 1000 THEN 'High'
ELSE 'VIP'

END segment

FROM spending;

--Разделяет клиентов на сегменты по общей сумме покупок.
--Показывает: клиента; общую сумму покупок; категорию клиента.
