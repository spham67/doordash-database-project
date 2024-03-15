#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2, datetime
import sys

def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')    

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

def show_all(table):
    print(f"Table: {table}")
    cur.execute("SELECT * FROM %s" % table)
    rows = cur.fetchall()
    for row in rows:
        print(row)

#------------------------------------------------------------
# show_menu
#------------------------------------------------------------

def show_menu():
    menu = '''

    
actions = { 1:add_to_favorites_menu,    2:add_item_menu,   3:see_dasher_average_menu,
            4:see_weekly_tips_menu,  5:see_popular_items_menu,
            6:place_order_menu, 7:browse_high_rating_restaurants_menus, 8: see_popular_areas,
            9: offer_coupons_menu, 10: rate_restaurant_menu}
--------------------------------------------------
1. Add Restaurant to Favorites List
2. Add Item to Menu
3. See Dasher's Average Rating 
4. See Dasher's Weekly Tips 
5. See Popular Items for Merchant
6. Place an order
7. Filter for High Rated Restaurants
8. See Popular Merchant Areas
9. Offer Coupon to Customer
10. Rate a Restaurant

Choose (1-10, 0 to quit): '''

    try:
        choice = int(input( menu ))
    except ValueError:
        print("\n\n* Invalid choice. Choose again.")
        show_menu()
    else:
        if choice == 0:
            print('Done.')
            cur.close()
            conn.close()
        elif choice in range(1,1+7):
            print()
            actions[choice]()
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close() 

#-----------------------------------------------------------------
# Add restaurant to user's favorite list
#-----------------------------------------------------------------

def add_to_favorites_menu():
    heading("Add to favorites")
    user_id = input('user_id: ')
    merc_id = input('merc_id: ')
    add_to_favorites(user_id, merc_id)

def add_to_favorites(user_id, merc_id):
    query = '''
        INSERT INTO Customer_Favorites(user_id, merc_id)
        VALUES(%s, %s)
    '''
    print(f"[add_to_favorites]\n  INSERT INTO Customer_Favorites(user_id, merc_id) \n  VALUES({user_id}, {merc_id})")
    cur.execute(query, (user_id, merc_id))
    show_all("Customer_Favorites")

#-----------------------------------------------------------------
# Rate a restaurant a user ordered from
#-----------------------------------------------------------------
    
def rate_restaurant_menu():
    heading("Rate restaurant")
    order_id = input('order_id: ')
    rating = input('rating: ')
    rate_restaurant(order_id, rating)

def rate_restaurant(order_id, rating):
    if 0 > rating or rating > 5 or int(rating) != rating: 
        print("Not a valid rating: must be an int in [0, 5]")
        return

    query = '''
        UPDATE Orders
        SET res_rating = %s
        WHERE order_id = %s
    '''
    print(f"[rate_restaurant]\n  UPDATE Orders\n  SET res_rating = {rating}\n  WHERE order_id = {order_id}")
    cur.execute(query, (rating, order_id))
    show_all("Orders")

#-----------------------------------------------------------------
# Add items to a merchant's menu
#-----------------------------------------------------------------
def add_item_menu():
    heading("Add item to a menu")
    name = input('Name: ')
    price = input('Price: ')
    description = input('Description:' ) 
    merc_id = input('merc_id:' ) 
    add_item(name, price, description, merc_id)

def add_item(name, price, description, merc_id):
    query = '''
        INSERT INTO Items(name, price, description, merc_id)
        VALUES(%s, %s, %s, %s)
    '''
    print(f"[add_items_to_menu]\n  INSERT INTO Items(name, price, description, merc_id)\n  VALUES({name}, {price}, {description}, {merc_id})")
    cur.execute(query, (name, price, description, merc_id))
    show_all("Items")

#-----------------------------------------------------------------
# See dashers average rating
#-----------------------------------------------------------------
def see_dasher_average_menu():
    heading("See Dasher Average")
    dasher_id = input('dasher_id: ')
    see_dasher_average_rating(dasher_id)

def see_dasher_average_rating(dasher_id):
    query = '''
        SELECT AVG(dasher_rating)
        FROM Orders
        WHERE dasher_id = %s
    '''
    print(f"[see_dasher_average_rating]\n  SELECT AVG(dasher_rating)\n  FROM Orders\n  WHERE dasher_id = {dasher_id}")
    cur.execute(query, (dasher_id,))
    rows = cur.fetchall()
    rating = rows[0][0]
    print(f"Average rating for dasher {dasher_id}: {rating}")

#-----------------------------------------------------------------
# See dashers weekly tips
#-----------------------------------------------------------------
def see_weekly_tips_menu():
    heading("See dasher weekly tips")
    dasher_id = input('dasher_id: ')
    see_weekly_tips(dasher_id)

def see_weekly_tips(dasher_id):
    now = datetime.datetime.now()
    for i in range(1, 5):
        prev = now - datetime.timedelta(i * 7) # datatime i weeks from now (check up to 4 weeks)
        nextt = now - datetime.timedelta((i - 1) * 7)
        print(f"-Week: {prev} ~ {nextt}")
        query = '''
            SELECT SUM(tip)
            FROM Orders
            WHERE dasher_id = %s
            AND date <= %s
            AND date >= %s
        '''
        print(f"[see_weekly_tips]\n  SELECT SUM(tip)\n  FROM Orders\n  WHERE dasher_id = {dasher_id}\n  AND date <= {nextt}\n  AND date >= {prev}")
        cur.execute(query, (dasher_id, nextt, prev))
        rows = cur.fetchall()
        for row in rows:
            print("Tip: ",row[0])

#-----------------------------------------------------------------
# See the most popular dishes being ordered for a given merchant
#-----------------------------------------------------------------
def see_popular_items_menu():
    heading("See popular items on menu")
    merc_id = input('merc_id: ')
    see_popular_items(merc_id)

def see_popular_items(merc_id):
    query = '''
        SELECT i1.name, COUNT(i1.item_id) 
        FROM Items as i1
        JOIN Items_Ordered as i2 ON i1.item_id = i2.item_id
        JOIN Orders as o ON i2.order_id = o.order_id
        WHERE o.merc_id = %s
        GROUP BY i1.item_id, i1.name
        ORDER BY COUNT(i1.item_id) DESC  
    '''
    print(f"[see_popular_items]\n  SELECT i1.name, COUNT(i1.item_id)\n  FROM Items as i1\n  JOIN Items_Ordered as i2 ON i1.item_id = i2.item_id\n  JOIN Orders as o ON i2.order_id = o.order_id\n  WHERE o.merc_id = {merc_id}\n  GROUP BY i1.item_id, i1.name\n  ORDER BY COUNT(i1.item_id) DESC")
    cur.execute(query, (merc_id,)) 
    rows = cur.fetchall()
    for row in rows:
        print(row)

#-----------------------------------------------------------------
# Place an order
#-----------------------------------------------------------------
def place_order_menu():
    heading("Place an order")
    user_id = input('user_id: ')
    merc_id = input('merc_id: ')
    dasher_id = input('dasher_id: ')
    item_id = input('item_id: ')
    quantity = input('quantity: ')
    place_order(user_id, merc_id, dasher_id, item_id, quantity)

def place_order(user_id, merc_id, dasher_id, item_id, quantity):
    # check if all item_ids indeed belongs to merc_id
    print("\nFirst make sure all items being ordered are indeed offered by the given merchant")
    query = '''
        SELECT *
        FROM Items
        WHERE item_id = %s
        AND merc_id = %s
    '''
    print(f"[place_order]\n  SELECT * FROM Items\n  WHERE item_id = {item_id} AND merc_id = {merc_id}")
    cur.execute(query, (item_id, merc_id))
    rows = cur.fetchall()
        
    # create a new order
    print("\nCreate a new order")
    now = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    query = '''
        INSERT INTO Orders(date, merc_id, user_id, dasher_id)
        VALUES (%s, %s, %s, %s)
    '''
    print(f"[place_order]\n  INSERT INTO Orders(date, merc_id, user_id, dasher_id)\n  VALUES ({now}, {merc_id}, {user_id}, {dasher_id})")
    cur.execute(query, (now, merc_id, user_id, dasher_id))

    # fetch the order_id
    print("\nGet the order_id generated for the new entry")
    query = '''
        SELECT order_id
        FROM Orders
        WHERE user_id = %s
        AND merc_id = %s
        AND date = %s
    '''
    print(f"[place_order]\n  SELECT order_id FROM Orders\n  WHERE user_id = {user_id} AND merc_id = {merc_id} AND date = {now}")
    cur.execute(query, (user_id, merc_id, now))
    rows = cur.fetchall()
    order_id = rows[0][0]
    print(f"--order_id = {order_id}")

    # insert item_id and corresponding quantity to Items_Ordered
    print("\nAdd all items and corresponding quantity to Items_Ordered")

    query = '''
        INSERT INTO Items_Ordered(item_id, order_id, quantity)
        VALUES (%s, %s, %s)
    '''
    print(f"[place_order]\n  INSERT INTO Items_Ordered(item_id, order_id, quantity)\n  VALUES ({item_id}, {order_id}, {quantity}")
    cur.execute(query, (item_id, order_id, quantity))

    # calculate total amount
    print("\nCalculate the totals of this order")
    query = '''
        SELECT SUM(i1.price * i2.quantity)
        FROM Items as i1
        JOIN Items_Ordered as i2 ON i1.item_id = i2.item_id
        WHERE i2.order_id = %s
    '''
    print(f"[place_order]\n  SELECT SUM(i1.price * i2.quantity) FROM Items as i1\n  JOIN Items_Ordered as i2 ON i1.item_id = i2.item_id\n  WHERE i2.order_id = {order_id}")
    cur.execute(query, (order_id,))
    rows = cur.fetchall()
    totals = rows[0][0]
    print(f"--totals = {totals}")

    # update user's account balance
    print("\nGet user's account balance and update it if necessary")
    query = '''
        SELECT balance
        FROM Customers
        WHERE user_id = %s
    '''
    print(f"[place_order]\n  SELECT balance FROM Customers WHERE user_id = {user_id}")
    cur.execute(query, (user_id,))
    rows = cur.fetchall()
    balance = rows[0][0]
    print(f"--account balance = {balance}")         
    amount = min(totals, balance)
    remain = max(0, totals - balance)
    
    query = '''
        UPDATE Customers
        SET balance = balance - %s
        WHERE user_id = %s
    '''
    print(f"[place_order]\n  UPDATE Customers\n  SET balance = balance - {amount} WHERE user_id = {user_id}")
    cur.execute(query, (amount, user_id))
    
    print(f"--${amount} deducted from account balance, current account balance: ${balance - amount}")
    print(f"--remaining totals to be paid: ${remain}")

    show_all("Orders")

#-----------------------------------------------------------------
# Browse high rated restaurants (4+)
#-----------------------------------------------------------------
def browse_high_rating_restaurants_menus():
    heading("Browse high rated restaurants")
    zipcode = input('zipcode: ')
    browse_high_rating_restaurants(zipcode)

def browse_high_rating_restaurants(zipcode):
    query = '''
        SELECT m.name, AVG(o.res_rating)
        FROM Merchants as m
        JOIN Orders as o ON o.merc_id = m.merc_id
        JOIN Addresses as a on a.addr_id = m.addr_id
        WHERE a.zipcode = %s
        GROUP BY m.merc_id
        HAVING AVG(o.res_rating) >= 4
        ORDER BY AVG(o.res_rating) DESC
    '''
    print(f"[browse_high_rating_restaurants]\n  SELECT m.name FROM Merchants as m\n  JOIN Orders as o ON o.merc_id = m.merc_id\n  JOIN Addresses as a on a.addr_id = m.addr_id\n  WHERE a.zipcode = {zipcode}\n  GROUP BY m.merc_id HAVING AVG(o.res_rating) >= 4")
    cur.execute(query, (zipcode,))
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]}: average rating {row[1]}")

#-----------------------------------------------------------------
# See most popular areas (in terms of number of orders)
#-----------------------------------------------------------------
def see_popular_areas():
    query = '''
        SELECT a.zipcode, COUNT(o.order_id)
        FROM Addresses as a
        JOIN Merchants as m on m.addr_id = a.addr_id
        JOIN Orders as o on o.merc_id = m.merc_id
        GROUP BY a.zipcode
        ORDER BY COUNT(o.order_id) DESC
    '''
    print(f"[see_popular_areas]\n  SELECT a.zipcode, COUNT(o.order_id) FROM Addresses as a\n  JOIN Merchants as m on m.addr_id = a.addr_id\n  JOIN Orders as o on o.merc_id = m.merc_id\n  GROUP BY a.zipcode\n  ORDER BY COUNT(o.order_id) DESC")
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(f"zipcode: {row[0]}, number of orders: {row[1]}")

#-----------------------------------------------------------------
# Offer coupons for loyal customers
#-----------------------------------------------------------------
def offer_coupons_menu():
    heading("Offer Coupon")
    n = input('Number coupons: ')
    merc_id = input('merc_id: ')
    coupon_type = input('coupon_type: ')
    min_price = input('min_price: ')
    exp_date = input('exp_date: ')
    amount = input('amount: ')
    percentage = input('percentage: ')
    max_amount = input('max_amount: ')
    offer_coupons(n, merc_id, coupon_type, min_price, exp_date, amount, percentage, max_amount)

def offer_coupons(n, merc_id, coupon_type, min_price, exp_date, amount=0, percentage=0, max_amount=0):
    # add coupon info
    print(f"\nAdd a new {coupon_type} coupon for merchant {merc_id}, eligible for all customers who have ordered {n} times or more")
    query = '''
        INSERT INTO Coupons(min_price, exp_date, merc_id)
        VALUES (%s, %s, %s)
    '''
    print(f"[offer_coupons]\n  INSERT INTO Coupons(min_price, exp_date, merc_id)\n  VALUES ({min_price}, {exp_date}, {merc_id})")
    cur.execute(query, (min_price, exp_date, merc_id))
    
    # get coupon_id
    print("\nGet the coupon_id generated for the new entry")
    query = '''
        SELECT coupon_id
        FROM Coupons
        WHERE min_price = %s
        AND exp_date = %s
        AND merc_id = %s
    '''
    print(f"[offer_coupons]\n  SELECT coupon_id FROM Coupons\n  WHERE min_price = {min_price} AND exp_date = {exp_date} AND merc_id = {merc_id}")
    cur.execute(query, (min_price, exp_date, merc_id))
    rows = cur.fetchall()
    coupon_id = rows[0][0]
    print(f"--coupon_id = {coupon_id}")

    if coupon_type == "fixed":
        print("\nAdd a fixed coupon")
        query = '''
            INSERT INTO Fixed_Coupons(coupon_id, amount)
            VALUES(%s, %s)
        '''
        print(f"[offer_coupons]\n  INSERT INTO Fixed_Coupons(coupon_id, amount)\n  VALUES({coupon_id}, {amount})")
        cur.execute(query, (coupon_id, amount))

    elif coupon_type == "percentage":
        print("\nAdd a percentage coupon")
        query = '''
            INSERT INTO Percentage_Coupons(coupon_id, percentage, max_amount)
            VALUES(%s, %s, %s)
        '''
        print(f"[offer_coupons]\n  INSERT INTO Percentage_Coupons(coupon_id, percentage, max_amount)\n  VALUES({coupon_id}, {percentage}, {max_amount})")
        cur.execute(query, (coupon_id, percentage, max_amount))
    else:
        print("Invalid coupon type: must be either fixed or percentage")
        return


    # find all customers who have ordered at a given merchant for more than n times 
    print("\nFind all eligible customers")
    query = '''
        SELECT o.user_id
        FROM Customers as c
        JOIN Orders as o on o.user_id = c.user_id
        WHERE o.merc_id = %s
        GROUP BY o.user_id
        HAVING COUNT(o.order_id) >= %s
    '''
    print(f"[offer_coupons]\n  SELECT o.user_id FROM Customers as c\n  JOIN Orders as o on o.user_id = c.user_id\n  WHERE o.merc_id = {merc_id}\n  GROUP BY o.user_id HAVING COUNT(o.order_id) >= {n}")
    cur.execute(query, (merc_id, n))
    rows = cur.fetchall()

    # add the coupon to all such customers
    print("\nAdd the coupon for all eligible customers")
    for row in rows:
        user_id = row[0]
        query = '''
            INSERT INTO Customer_Coupons(user_id, coupon_id)
            VALUES(%s, %s)
        '''
        print(f"[offer_coupons]\n  INSERT INTO Customer_Coupons(user_id, coupon_id)\n  VALUES({user_id}, {coupon_id})")
        cur.execute(query, (user_id, coupon_id))

    show_all("Coupons")
    show_all("Customer_Coupons")

    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:add_to_favorites_menu,    2:add_item_menu,   3:see_dasher_average_menu,
            4:see_weekly_tips_menu,  5:see_popular_items_menu,
            6:place_order_menu, 7:browse_high_rating_restaurants_menus, 8: see_popular_areas,
            9: offer_coupons_menu, 10: rate_restaurant_menu}


if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'doordash', 'isdb'
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        # by assigning to conn and cur here they become
        # global variables.  Hence they are not passed
        # into the various SQL interface functions
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        show_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))
