\c postgres
DROP DATABASE IF EXISTS doordash;

CREATE database doordash;
\c doordash

\i create.SQL


\copy Customers(fname, lname, phone, email, country, password, balance) FROM 'customers.csv' csv header
\copy Dashers(fname, lname, delivery_mode) FROM 'dashers.csv' csv header
\copy Addresses(address, zipcode) FROM 'addresses.csv' csv header
\copy Merchants(name, addr_id) FROM 'merchants.csv' csv header
\copy Items(name, price, description, merc_id) FROM 'items.csv' csv header
\copy Orders(date, tip, res_rating, dasher_rating, merc_id, user_id, dasher_id) FROM 'orders.csv' csv header
\copy Payment_Methods(card_number, exp_date, cvv, user_id) FROM 'payment_methods.csv' csv header
\copy Regular_Customers(user_id) FROM 'regular_customers.csv' csv header
\copy Premium_Customers(user_id, end_date, monthly_rate) FROM 'premium_customers.csv' csv header
\copy Coupons(min_price, exp_date, merc_id) FROM 'coupons.csv' csv header
\copy Fixed_Coupons(coupon_id, amount) FROM 'fixed_coupons.csv' csv header
\copy Percentage_Coupons(coupon_id, percentage, max_amount) FROM 'percentage_coupons.csv' csv header
\copy Customer_Addresses(user_id, addr_id) FROM 'customer_addresses.csv' csv header
\copy Customer_Favorites(user_id, merc_id) FROM 'customer_favorites.csv' csv header
\copy Customer_Coupons(user_id, coupon_id) FROM 'customer_coupons.csv' csv header
\copy Items_Ordered(item_id, order_id, quantity) FROM 'items_ordered.csv' csv header

