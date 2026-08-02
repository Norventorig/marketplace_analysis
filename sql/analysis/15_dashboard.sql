SELECT
	DATE_TRUNC('year',o.order_purchase_timestamp) AS year,
	DATE_TRUNC('month',o.order_purchase_timestamp) AS month,
	SUM(oi.price) AS revenue,
	COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN order_items oi USING(order_id)
GROUP BY GROUPING SETS(
	(DATE_TRUNC('year',o.order_purchase_timestamp)),
	(DATE_TRUNC('month',o.order_purchase_timestamp)),
	()
)
ORDER BY year, month;

--Формирует сводный аналитический отчет по продажам.
--Показывает: выручку по годам; выручку по месяцам; общий итог по всем данным; количество заказов.
