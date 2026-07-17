CREATE TABLE IF NOT EXISTS customers
    (
    customer_id VARCHAR (32) NOT NULL,
    customer_unique_id VARCHAR(32) NOT NULL,
    customer_city VARCHAR(32) NOT NULL,
    customer_state VARCHAR(2) NOT NULL,
    customer_zip_code_prefix VARCHAR(5)
    );

CREATE TABLE IF NOT EXISTS geolocation
    (
    geolocation_zip_code_prefix VARCHAR (5) NOT NULL,
    geolocation_lat DOUBLE PRECISION NOT NULL,
    geolocation_lng DOUBLE PRECISION NOT NULL,
    geolocation_city VARCHAR (64) NOT NULL,
    geolocation_state VARCHAR (2) NOT NULL
    );

CREATE TABLE IF NOT EXISTS order_items
    (
    order_item_id SMALLINT NOT NULL,
    order_id VARCHAR (32) NOT NULL,
    shipping_limit_date TIMESTAMP,
    price NUMERIC (10, 2) NOT NULL,
    freight_value NUMERIC (10, 2) NOT NULL,
    product_id VARCHAR (32),
    seller_id VARCHAR (32)
    );

CREATE TABLE IF NOT EXISTS order_payments
    (
    payment_sequential SMALLINT NOT NULL,
    payment_type VARCHAR (20) NOT NULL,
    payment_installments SMALLINT NOT NULL,
    payment_value NUMERIC (10, 2) NOT NULL,
    order_id VARCHAR (32) NOT NULL
    );

CREATE TABLE IF NOT EXISTS order_reviews
    (
    review_id VARCHAR (32) NOT NULL,
    review_score SMALLINT NOT NULL,
    review_comment_title VARCHAR (255),
    review_comment_message TEXT,
    review_creation_date TIMESTAMP NOT NULL,
    review_answer_timestamp TIMESTAMP,
    order_id VARCHAR (32) NOT NULL
    );

CREATE TABLE IF NOT EXISTS orders
    (
    order_id VARCHAR (32) NOT NULL,
    order_status VARCHAR (16) NOT NULL,
    order_purchase_timestamp TIMESTAMP NOT NULL,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP NOT NULL,
    customer_id VARCHAR (32)
    );

CREATE TABLE IF NOT EXISTS products
    (
    product_id VARCHAR (32) NOT NULL,
    product_category_name VARCHAR (64),
    product_name_lenght SMALLINT,
    product_description_lenght SMALLINT,
    product_photos_qty SMALLINT,
    product_weight_g INT,
    product_length_cm SMALLINT,
    product_height_cm SMALLINT,
    product_width_cm SMALLINT
    );

CREATE TABLE IF NOT EXISTS sellers
    (
    seller_id VARCHAR(32) NOT NULL,
    seller_city VARCHAR (64) NOT NULL,
    seller_state VARCHAR (2) NOT NULL,
    seller_zip_code_prefix VARCHAR(5)
    );

CREATE TABLE IF NOT EXISTS product_category_name_translation
    (
    product_category_name VARCHAR (64) NOT NULL,
    product_category_name_english VARCHAR (64) NOT NULL
    );