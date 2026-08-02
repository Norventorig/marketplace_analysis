SELECT
	pct.product_category_name_english,
	ROUND(SUM(oi.price), 2) AS revenue
FROM products AS p

JOIN product_category_name_translation AS pct
USING (product_category_name)

JOIN order_items oi
USING (product_id)

GROUP BY pct.product_category_name_english
ORDER BY revenue DESC;

--Определяет наиболее прибыльные категории товаров.
--Показывает: категорию товара; общую выручку.
