SELECT
	c.customer_unique_id,
	COUNT(DISTINCT o.order_id) AS orders_amount
FROM customers AS c

JOIN orders AS o
USING (customer_id)

GROUP BY c.customer_unique_id

HAVING COUNT (DISTINCT o.order_id) > 1

ORDER BY orders_amount DESC;

--Находит клиентов, совершивших более одного заказа.
--Показывает: идентификатор клиента; количество оформленных заказов.
