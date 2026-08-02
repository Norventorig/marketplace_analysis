SELECT
	seller_state,
	seller_id,

	SUM(price) AS revenue,
	RANK() OVER(
	PARTITION BY seller_state
	ORDER BY SUM(price) DESC
	) state_rank
FROM sellers
JOIN order_items USING(seller_id)
GROUP BY seller_state, seller_id;

--Строит рейтинг продавцов внутри каждого штата.
--Показывает: штат; продавца; общую выручку; место продавца в рейтинге в пределах своего штата.
