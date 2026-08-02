SELECT
    seller_id,
    ROUND(SUM(price),2) revenue,
    RANK() OVER(
        ORDER BY SUM(price) DESC
    ) seller_rank
FROM order_items
GROUP BY seller_id
LIMIT 20;

--Определяет продавцов с наибольшей выручкой и строит их рейтинг.
--Показывает: продавца; общую выручку; место в рейтинге по объему продаж.
