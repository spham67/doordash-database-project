# Doordash Database Project
This project represents a basic data model of Doordash implemented using Python and PostgreSQL.

# Requirements
It is required to have PostgreSQL installed as well as the psycopg2 python module installed.  

pip install psycopg2

(OR) pip install psycopg2-binary

# User Stories
This database realizes these following user pain points:
1) As a Customer, I want to place order online and get it delivered to my door
2) As a Customer, I wish to add a restaurant to my favorite list
3) As a Customer, I want to rate the restaurant I ordered from
4) As a Customer, I want to browse all restaurants in my current zip code with 4+ average rating
5) As a Dasher, I want to see my average rating
6) As a Dasher, I want to see what are the most popular areas (in terms of number of orders)
7) As a Dasher, I want to check my weekly total tips for the past month
8) As a Merchant, I want to add items on my menu
9) As a Merchant, I want to see the most popular dishes being ordered
10) As a Merchant, I want to offer coupons for customers who have ordered at my restaurant over a certain number of times

# Entity Relationship Diagram
Data entities for Doordash's data model can be visualized in the following ERD:
<img width="1343" alt="image" src="https://github.com/spham67/doordash-database-project/assets/98799078/cade2d39-7e45-4adc-bdb7-d2a546b5e64f">

# How to run

1) Run initialize.sql (This file creates all tables, relationships, and loads example seed data from the seeds folder)
2) Run python3 queries.py (This will show a menu on cmd where directions are provided)
