-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2021-11-29 03:58:58.267
-- tables
-- Table: Addresses
CREATE TABLE Addresses (
    addr_id serial  NOT NULL,
    address text  NOT NULL,
    zipcode int  NOT NULL,
    CONSTRAINT Addresses_pk PRIMARY KEY (addr_id)
);

-- Table: Coupons
CREATE TABLE Coupons (
    coupon_id serial  NOT NULL,
    min_price decimal(15,2)  NOT NULL,
    exp_date date  NOT NULL,
    merc_id serial  NOT NULL,
    CONSTRAINT Coupons_pk PRIMARY KEY (coupon_id)
);

-- Table: Customer_Addresses
CREATE TABLE Customer_Addresses (
    user_id serial  NOT NULL,
    addr_id serial  NOT NULL,
    CONSTRAINT Customer_Addresses_pk PRIMARY KEY (user_id,addr_id)
);

-- Table: Customer_Coupons
CREATE TABLE Customer_Coupons (
    user_id serial  NOT NULL,
    coupon_id serial  NOT NULL,
    CONSTRAINT Customer_Coupons_pk PRIMARY KEY (user_id,coupon_id)
);

-- Table: Customer_Favorites
CREATE TABLE Customer_Favorites (
    user_id serial  NOT NULL,
    merc_id serial  NOT NULL,
    CONSTRAINT Customer_Favorites_pk PRIMARY KEY (user_id,merc_id)
);

-- Table: Customers
CREATE TABLE Customers (
    user_id serial  NOT NULL,
    fname text  NOT NULL,
    lname text  NOT NULL,
    phone varchar(10)  NOT NULL,
    email text  NOT NULL,
    country text  NOT NULL,
    password varchar(20)  NOT NULL,
    balance decimal(15,2)  NOT NULL,
    CONSTRAINT Customers_pk PRIMARY KEY (user_id)
);

-- Table: Dashers
CREATE TABLE Dashers (
    dasher_id serial  NOT NULL,
    fname text  NOT NULL,
    lname text  NOT NULL,
    delivery_mode text  NOT NULL,
    CONSTRAINT Dashers_pk PRIMARY KEY (dasher_id)
);

-- Table: Fixed_Coupons
CREATE TABLE Fixed_Coupons (
    coupon_id serial  NOT NULL,
    amount decimal(15,2)  NOT NULL,
    CONSTRAINT Fixed_Coupons_pk PRIMARY KEY (coupon_id)
);

-- Table: Items
CREATE TABLE Items (
    item_id serial  NOT NULL,
    name text  NOT NULL,
    price decimal(15,2)  NOT NULL,
    description text  NOT NULL,
    merc_id serial  NOT NULL,
    CONSTRAINT Items_pk PRIMARY KEY (item_id)
);

-- Table: Items_Ordered
CREATE TABLE Items_Ordered (
    item_id serial  NOT NULL,
    order_id serial  NOT NULL,
    quantity int  NOT NULL,
    CONSTRAINT Items_Ordered_pk PRIMARY KEY (item_id,order_id)
);

-- Table: Merchants
CREATE TABLE Merchants (
    merc_id serial  NOT NULL,
    name text  NOT NULL,
    addr_id serial  NOT NULL,
    CONSTRAINT Merchants_pk PRIMARY KEY (merc_id)
);

-- Table: Orders
CREATE TABLE Orders (
    order_id serial  NOT NULL,
    date timestamp  NOT NULL,
    tip decimal(15,2),
    res_rating int,
    dasher_rating int,
    merc_id serial  NOT NULL,
    user_id serial  NOT NULL,
    dasher_id serial  NOT NULL,
    CONSTRAINT Orders_pk PRIMARY KEY (order_id)
);

-- Table: Payment_Methods
CREATE TABLE Payment_Methods (
    card_number int  NOT NULL,
    exp_date date  NOT NULL,
    cvv int  NOT NULL,
    user_id serial  NOT NULL,
    CONSTRAINT Payment_Methods_pk PRIMARY KEY (card_number)
);

-- Table: Percentage_Coupons
CREATE TABLE Percentage_Coupons (
    coupon_id serial  NOT NULL,
    percentage int  NOT NULL,
    max_amount decimal(15,2)  NOT NULL,
    CONSTRAINT Percentage_Coupons_pk PRIMARY KEY (coupon_id)
);

-- Table: Premium_Customers
CREATE TABLE Premium_Customers (
    user_id serial  NOT NULL,
    end_date date  NOT NULL,
    monthly_rate decimal(15,2)  NOT NULL,
    CONSTRAINT Premium_Customers_pk PRIMARY KEY (user_id)
);

-- Table: Regular_Customers
CREATE TABLE Regular_Customers (
    user_id serial  NOT NULL,
    CONSTRAINT Regular_Customers_pk PRIMARY KEY (user_id)
);

-- foreign keys
-- Reference: Coupons_Merchants (table: Coupons)
ALTER TABLE Coupons ADD CONSTRAINT Coupons_Merchants
    FOREIGN KEY (merc_id)
    REFERENCES Merchants (merc_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Addresses_Addresses (table: Customer_Addresses)
ALTER TABLE Customer_Addresses ADD CONSTRAINT Customer_Addresses_Addresses
    FOREIGN KEY (addr_id)
    REFERENCES Addresses (addr_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Addresses_Customers (table: Customer_Addresses)
ALTER TABLE Customer_Addresses ADD CONSTRAINT Customer_Addresses_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Coupons_Coupons (table: Customer_Coupons)
ALTER TABLE Customer_Coupons ADD CONSTRAINT Customer_Coupons_Coupons
    FOREIGN KEY (coupon_id)
    REFERENCES Coupons (coupon_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Coupons_Customers (table: Customer_Coupons)
ALTER TABLE Customer_Coupons ADD CONSTRAINT Customer_Coupons_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Favorites_Customers (table: Customer_Favorites)
ALTER TABLE Customer_Favorites ADD CONSTRAINT Customer_Favorites_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Favorites_Merchants (table: Customer_Favorites)
ALTER TABLE Customer_Favorites ADD CONSTRAINT Customer_Favorites_Merchants
    FOREIGN KEY (merc_id)
    REFERENCES Merchants (merc_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Fixed_Coupons_Coupons (table: Fixed_Coupons)
ALTER TABLE Fixed_Coupons ADD CONSTRAINT Fixed_Coupons_Coupons
    FOREIGN KEY (coupon_id)
    REFERENCES Coupons (coupon_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Items_Merchants (table: Items)
ALTER TABLE Items ADD CONSTRAINT Items_Merchants
    FOREIGN KEY (merc_id)
    REFERENCES Merchants (merc_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Items_Ordered_Items (table: Items_Ordered)
ALTER TABLE Items_Ordered ADD CONSTRAINT Items_Ordered_Items
    FOREIGN KEY (item_id)
    REFERENCES Items (item_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Items_Ordered_Orders (table: Items_Ordered)
ALTER TABLE Items_Ordered ADD CONSTRAINT Items_Ordered_Orders
    FOREIGN KEY (order_id)
    REFERENCES Orders (order_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Merchants_Addresses (table: Merchants)
ALTER TABLE Merchants ADD CONSTRAINT Merchants_Addresses
    FOREIGN KEY (addr_id)
    REFERENCES Addresses (addr_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Customers (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Dashers (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Dashers
    FOREIGN KEY (dasher_id)
    REFERENCES Dashers (dasher_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Merchants (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Merchants
    FOREIGN KEY (merc_id)
    REFERENCES Merchants (merc_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Payment_Methods_Customers (table: Payment_Methods)
ALTER TABLE Payment_Methods ADD CONSTRAINT Payment_Methods_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Percentage_Coupons_Coupons (table: Percentage_Coupons)
ALTER TABLE Percentage_Coupons ADD CONSTRAINT Percentage_Coupons_Coupons
    FOREIGN KEY (coupon_id)
    REFERENCES Coupons (coupon_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Premium_Customers_Customers (table: Premium_Customers)
ALTER TABLE Premium_Customers ADD CONSTRAINT Premium_Customers_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Regular_Customers_Customers (table: Regular_Customers)
ALTER TABLE Regular_Customers ADD CONSTRAINT Regular_Customers_Customers
    FOREIGN KEY (user_id)
    REFERENCES Customers (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

