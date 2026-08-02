SELECT
	customer_state,
	COUNT(DISTINCT customer_unique_id) AS customers,
	COUNT(order_id) AS orders,
	ROUND(SUM(price), 2) AS revenue
FROM customers
JOIN orders USING(customer_id)
JOIN order_items USING(order_id)
GROUP BY customer_state
ORDER BY revenue DESC;

--Анализирует продажи по штатам покупателей.
--Показывает: количество клиентов; количество заказов; общую выручку.
