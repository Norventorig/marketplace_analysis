SELECT
	product_id,
	COUNT(*) AS sold_amount,
	
	DENSE_RANK() OVER(
	ORDER BY COUNT(*) DESC
	) AS ranking

FROM order_items
GROUP BY product_id
LIMIT 20;

--Строит рейтинг наиболее продаваемых товаров.
--Показывает: товар; количество продаж; место в рейтинге.
