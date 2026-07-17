CREATE INDEX idx_orders_purchase_timestamp
ON orders(order_purchase_timestamp);

CREATE INDEX idx_orders_customer_id
ON orders(customer_id);

CREATE INDEX idx_order_items_product_id
ON order_items(product_id);

CREATE INDEX idx_order_items_seller_id
ON order_items(seller_id);