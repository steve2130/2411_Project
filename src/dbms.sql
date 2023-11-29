DROP TABLE users;
DROP TABLE addresses;
DROP TABLE categories;
DROP TABLE products;
DROP TABLE product_skus;
DROP TABLE cart_items;
DROP TABLE orders;
DROP TABLE order_items;



CREATE TABLE users (
  id number(10) PRIMARY KEY,
  username varchar2(255),
  avatar_url varchar2(255),
  password varchar2(255),
  is_admin char(1)
);


CREATE TABLE addresses (
  id number(10) PRIMARY KEY,
  user_id number(10),
  details clob
);


CREATE TABLE categories (
  id number(10) PRIMARY KEY,
  name varchar2(255)
);


CREATE TABLE products (
  id number(10) PRIMARY KEY,
  category_id number(10),
  title varchar2(255),
  description clob,
  image_url varchar2(255),
  lowest_price number(10,0)
);


CREATE TABLE product_skus (
  id number(10) PRIMARY KEY,
  product_id number(10),
  title varchar2(255),
  description clob,
  price number(10,0),
  stock number(10)
);


CREATE TABLE cart_items (
  id number(10) PRIMARY KEY,
  user_id number(10),
  product_sku_id number(10),
  amount number(10)
);


CREATE TABLE orders (
  id number(10) PRIMARY KEY,
  user_id number(10),
  address_id number(10),
  total_amount number(10),
  remark varchar2(255),
  paid_at timestamp(0),
  payment_method varchar2(255),
  payment_no varchar2(255),
  shipment_status varchar2(255),
  shipment_dataa varchar2(255),
  refund_status varchar2(255),
  refund_no varchar2(255),
  closed char(1)
);


CREATE TABLE order_items (
  id number(10) PRIMARY KEY,
  order_id number(10),
  product_id number(10),
  product_sku_id number(10),
  price number(10,0),
  amount number(10)
);

ALTER TABLE addresses ADD FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE products ADD FOREIGN KEY (category_id) REFERENCES categories (id);

ALTER TABLE product_skus ADD FOREIGN KEY (product_id) REFERENCES products (id);

ALTER TABLE cart_items ADD FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE cart_items ADD FOREIGN KEY (product_sku_id) REFERENCES product_skus (id);

ALTER TABLE order_items ADD FOREIGN KEY (order_id) REFERENCES orders (id);

ALTER TABLE orders ADD FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE order_items ADD FOREIGN KEY (product_id) REFERENCES products (id);

ALTER TABLE order_items ADD FOREIGN KEY (product_sku_id) REFERENCES product_skus (id);

ALTER TABLE orders ADD FOREIGN KEY (address_id) REFERENCES addresses (id);

