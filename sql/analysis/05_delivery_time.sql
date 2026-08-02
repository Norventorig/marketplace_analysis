SELECT
	AVG(order_delivered_customer_date-order_purchase_timestamp)
	AS avg_delivery_time,
	
	MIN(order_delivered_customer_date-order_purchase_timestamp)
	AS min_delivery_time,
	
	MAX(order_delivered_customer_date-order_purchase_timestamp)
	AS max_delivery_time
FROM orders

WHERE order_status='delivered'
GROUP BY order_status;

--Вычисляет статистику по времени доставки заказов.
--Показывает: среднее время доставки; минимальное время доставки; максимальное время доставки.
