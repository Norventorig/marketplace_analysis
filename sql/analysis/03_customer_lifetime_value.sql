SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS orders_amount,
    ROUND(SUM(oi.price), 2) AS total_spent,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM customers c

JOIN orders AS o
USING (customer_id)

JOIN order_items AS oi
USING (order_id)

GROUP BY c.customer_unique_id
ORDER BY total_spent DESC;

--Рассчитывает основные показатели каждого клиента (Customer Lifetime Value).
--Показывает: количество заказов; общую сумму покупок; среднюю стоимость товара.
