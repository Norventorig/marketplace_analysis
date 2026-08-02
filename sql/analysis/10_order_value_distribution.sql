WITH orders_sum AS(
	SELECT
		order_id,
		SUM(price) AS total
	FROM order_items
	GROUP BY order_id
)

SELECT
	order_id,
	total,

	NTILE(10)
	OVER(
	ORDER BY total DESC
	) AS decile
FROM orders_sum;

--Распределяет заказы по децилям в зависимости от их стоимости.
--Показывает: заказ; стоимость заказа; дециль.
