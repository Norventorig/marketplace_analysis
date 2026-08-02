SELECT
	payment_type,
	COUNT(*) AS payments_amout,
	ROUND(SUM(payment_value), 2) AS total,
	ROUND(AVG(payment_value) FILTER (WHERE payment_value > 0), 2) AS avg_payment
FROM order_payments
GROUP BY payment_type
ORDER BY total DESC;

--Выводит данные о каждом типе оплаты.
--Показывает: количество платежей; общую сумму платежей; средний размер платежа.
