ALTER TABLE customers
ADD CONSTRAINT PK_customers PRIMARY KEY (customer_id);

ALTER TABLE geolocation
ADD CONSTRAINT PK_geolocation PRIMARY KEY (geolocation_id);

ALTER TABLE products
ADD CONSTRAINT PK_products PRIMARY KEY (product_id),

ADD CONSTRAINT CHK_products_product_name_lenght CHECK (product_name_lenght > 0),
ADD CONSTRAINT CHK_products_product_description_lenght CHECK (product_description_lenght > 0),
ADD CONSTRAINT CHK_products_product_photos_qty CHECK (product_photos_qty >= 0),
ADD CONSTRAINT CHK_products_product_weight_g CHECK (product_weight_g >= 0),
ADD CONSTRAINT CHK_products_product_length_cm CHECK (product_length_cm >= 0),
ADD CONSTRAINT CHK_products_product_height_cm CHECK (product_height_cm >= 0),
ADD CONSTRAINT CHK_products_product_width_cm CHECK (product_width_cm >= 0);


ALTER TABLE sellers
ADD CONSTRAINT PK_sellers PRIMARY KEY (seller_id);


ALTER TABLE orders
ADD CONSTRAINT PK_orders PRIMARY KEY (order_id),

ADD CONSTRAINT FK_orders_customers FOREIGN KEY (customer_id) REFERENCES customers (customer_id),

ADD CONSTRAINT CHK_orders_order_status CHECK (order_status IN ('delivered', 'invoiced', 'shipped', 'processing', 'unavailable', 'canceled', 'created', 'approved'));


ALTER TABLE order_items
ADD CONSTRAINT PK_order_items PRIMARY KEY (order_id, order_item_id),

ADD CONSTRAINT FK_order_items_products FOREIGN KEY (product_id) REFERENCES products (product_id),
ADD CONSTRAINT FK_order_items_sellers FOREIGN KEY (seller_id) REFERENCES sellers (seller_id),
ADD CONSTRAINT FK_order_items_orders FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,

ADD CONSTRAINT CHK_order_items_order_item_id CHECK (order_item_id > 0),
ADD CONSTRAINT CHK_order_items_price CHECK (price >= 0),
ADD CONSTRAINT CHK_order_items_freight_value CHECK (freight_value >= 0);


ALTER TABLE order_payments
ADD CONSTRAINT PK_order_payments PRIMARY KEY (order_id, payment_sequential),

ADD CONSTRAINT FK_order_payments_orders FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,

ADD CONSTRAINT CHK_order_payments_payment_sequential CHECK (payment_sequential >= 1),
ADD CONSTRAINT CHK_order_payments_payment_type CHECK (payment_type IN ('credit_card', 'boleto', 'voucher', 'debit_card', 'not_defined')),
ADD CONSTRAINT CHK_order_payments_payment_installments CHECK (payment_installments >= 0),
ADD CONSTRAINT CHK_order_payments_payment_value CHECK (payment_value >= 0);


ALTER TABLE order_reviews
ADD CONSTRAINT PK_order_reviews PRIMARY KEY (review_id, order_id),

ADD CONSTRAINT FK_order_reviews_orderS FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,

ADD CONSTRAINT CHK_order_reviews_review_score CHECK (review_score BETWEEN 0 AND 5);


ALTER TABLE product_category_name_translation
ADD CONSTRAINT PK_product_category_name_translation PRIMARY KEY (product_category_name);