\c doordash 

\echo "Customers: Customer Info";
select * from Customers;
\echo "Dashers: Dasher Info";
select * from Dashers;
\echo "Addresses: Address Info"; 
select * from Addresses;
\echo "Merchants: Merchant Info";
select * from Merchants;
\echo "Items: Items Offered By All Merchants";
select * from Items;
\echo "Orders: Orders Placed By All Customers";
select * from Orders;
\echo "Payment_Methods: Payment Methods For Each Customer";
select * from Payment_Methods;
\echo "Regular_Customers: Regular Customers Info";
select * from Regular_Customers;
\echo "Premium_Customers: Premium Customers Info";
select * from Premium_Customers;
\echo "Coupons: All Existing Coupon Info";
select * from Coupons;
\echo "Fixed_Coupons: Fixed Coupons Info";
select * from Fixed_Coupons;
\echo "Percentage_Coupons: Percentage Coupons Info";
select * from Percentage_Coupons;
\echo "Customer_Addresses: Addresses For Each Customer";
select * from Customer_Addresses;
\echo "Customer_Favorites: Favorite Merchants For Each Customer";
select * from Customer_Favorites;
\echo "Customer_Coupons: Coupons Owned By Each Customer";
select * from Customer_Coupons;
\echo "Items_Ordered: Items Included In Each Order";
select * from Items_Ordered;