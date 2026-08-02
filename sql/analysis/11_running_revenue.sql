WITH daily AS(
	SELECT
		DATE(order_purchase_timestamp) AS day,
		SUM(price) AS revenue
	FROM orders
	JOIN order_items USING(order_id)
	GROUP BY day
)

SELECT
	day,
	revenue,
	
	SUM(revenue)
	OVER(
	ORDER BY day
	) AS cumulative_revenue
FROM daily;

--Строит накопительную выручку по дням.
--Показывает: дату; дневную выручку; накопительную выручку.
