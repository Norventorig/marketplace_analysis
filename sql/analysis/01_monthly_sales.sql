WITH sales AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS date,
        oi.price
    FROM orders AS o
    JOIN order_items AS oi 
	USING(order_id)
    WHERE o.order_status='delivered'
)

SELECT
    EXTRACT(YEAR FROM date) as year,
    EXTRACT(MONTH FROM date) as month,
    COUNT(*) AS sold_items,
    ROUND(SUM(price),2) AS revenue,
    ROUND(AVG(price),2) AS avg_item_price
FROM sales
GROUP BY year, month
ORDER BY year, month;

--Анализирует динамику продаж по месяцам.
--Показывает: количество проданных товаров; общую выручку; среднюю стоимость товара.
