# from django.forms import Input
import pymysql
from posixpath import split

db = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="19990125jackk",
    database="retailshop"
)


def main():
    print("Here is the function menu:")
    print("1) Show All shops")
    print("2) Show All items")
    print("3) Create a shop")
    print("4) Create a item")
    print("5) Search item")
    print("6) Purchase item")
    print("7) Cancel order")
    print("8) Exit system")
    print("=====end=====")
    num = input("Please enter the function num:")
    if num == '1':
        showShops()
    elif num == '2':
        showItem()
        main()
    elif num == '3':
        addShop()
    elif num == '4':
        addItem()
    elif num == '5':
        search()
    elif num == '6':
        Item_purchase()
    elif num == '7':
        Order_cancel()
    elif num == '8':
        conclude()
        print("Exit the system")
    else:
        print("Error input")
        main()


def showShops():
    sql = "SELECT * FROM shops"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print("Here are all the shops in our system:")
        for res in result:
            print("sid:", res[0], " name:", res[1], " rating:", res[2], " location:", res[3])
    except:
        print("Error: unable to fetch data")
    print("=====end=====")
    main()


def showItem():
    sql = "SELECT * FROM items, shops WHERE items.sid = shops.sid"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print("Here are all the items in our system:")
        for res in result:
            print("iid:", res[0], " item_name:", res[2], " price:", res[3],
                  " quantity:", res[4], " shop_name:", res[9],
                  " keywords:", res[5], res[6], res[7])
    except:
        print("Error: unable to fetch data")
    print("=====end=====")


def addShop():
    try:
        sid = input("Input the sid: ")
        sname = input("Input the sname: ")
        rating = input("Input the rating: ")
        location = input("Input the location: ")
        sql = "insert into shops value('%s','%s','%s','%s')" % (str(sid),sname,int(rating),location)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to add data")
    print("=====end=====")
    main()

def addItem():
    try:
        iid = input("Input the iid: ")
        sid = input("Input the sid: ")
        iname = input("Input the iname: ")
        price = input("Input the price: ")
        quantity = input("Input the quantity: ")
        key1 = input("Input the key1: ")
        key2 = input("Input the key2: ")
        key3 = input("Input the key3: ")
        sql = "insert into items value('%s','%s','%s','%s','%s','%s','%s','%s')" % (str(iid),str(sid),iname,int(price),int(quantity),key1,key2,key3)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to add data")
    print("=====end=====")
    main()

def search():
    flag = 1
    while flag:
        print("What kinds of items you want to search?")
        keyw = input("Input the item feature: ")
        sql = "SELECT * FROM items,shops WHERE items.sid = shops.sid AND (iname = %s OR key1 = %s OR key2 = %s OR key3 = %s)"
        cursor = db.cursor()
        try:
            cursor.execute(sql, [str(keyw), str(keyw), str(keyw), str(keyw)])
            result = cursor.fetchall()
            if len(result) > 0:
                print("Here are all the records for searching:")
                for res in result:
                    print("iid:", res[0], " item_name:", res[2], " price:", res[3],
                          " quantity:", res[4], " shop_name:", res[9],
                          " keywords:", res[5], res[6], res[7])
            else:
                print("No Corresponding records")
            ans = int(input("Continue Searching: Yes:1 No:2\n"))
            if ans == 2:
                flag = 0
        except:
            print("Error: unable to fetch data")
            flag = 0
    print("=====end=====")
    main()


def show_user_orders(userinfo):
    sql = "SELECT * FROM orders WHERE cid = %s"
    cursor = db.cursor()
    try:
        cursor.execute(sql, userinfo)
        result = cursor.fetchall()
        if len(result) > 0:
            print("Here are your orders in our system:")
            for res in result:
                print("id:",res[0],"order_id:", res[1], " Customer_id:", res[2], " Item_id:", res[3]," Amount:", res[4])
            return 1
        else:
            print("You haven't made any orders so you can't cancel")
            return 0
    except:
        print("Error: unable to fetch data")
    print("=====end=====")


def showorders():
    sql = "SELECT * FROM orders"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print("Here are all the orders in our system:")
        for res in result:
            print("id:",res[0],"order_id:", res[1], " Customer_id:", res[2], " Item_id:", res[3]," Amount:", res[4])
    except:
        print("Error: unable to fetch data")
    print("=====end=====")


def creatid():
    sql = "SELECT * FROM orders"
    cursor = db.cursor()

    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        new_id = 1
    else:
        res = result[len(result) - 1]
        new_id = int(res[0]) + 1
    return new_id

def createoid():
    sql = "SELECT * FROM orders"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        new_oid = 1
    else:
        res = result[len(result) - 1]
        temp_list = res[1].split('O')
        new_oid = int(temp_list[1]) + 1
    return new_oid


# def Item_purchase():
#     flag = 1
#     while flag:
#         user_info = input("Please enter your customer id:")
#         print("Here are all Items and What items you want to buy?")
#         showItem()
#         keyw = input("Input your Puchasing items ID(if many items once need with blank space for each item): ")
#         willing_buying_list = keyw.split()
#         for item in willing_buying_list:
#             new_id = creatoid()
#             if new_id:
#                 sql = "INSERT INTO orders VALUES (%s,%s,%s)"
#                 sql_2 = "UPDATE items SET quantity = quantity - 1 WHERE iid = %s"
#                 cursor = db.cursor()
#                 try:
#                     cursor.execute(sql, [int(new_id), int(user_info), int(item)])
#                     cursor.execute(sql_2, int(item))
#                     db.commit()
#                 except:
#                     db.rollback()
#             else:
#                 print("New Order Create defeat")
#         ans = int(input("Continue Buying: Yes:1 No:2\n"))
#         if ans == 2:
#             flag = 0
#     print("=====end=====")


def Item_purchase():
    user_info = input("Please enter your customer id:")
    print("Here are all Items and What items you want to buy?")
    showItem()
    end = True
    items = []
    amount = []
    while end:
        keyw = input("Input your Purchasing items ID: ")
        num = input("Input the amount of the item you want purchase: ")
        items.append(keyw)
        amount.append(num)
        res = int(input("Continue Purchasing: Yes:1 No:2\n"))
        if res == 2:
            end = False

    new_oid = "O" + str(createoid())
    for i in range(0, len(items)):
        new_id = creatid()
        sql = "INSERT orders VALUES (%s,%s,%s,%s,%s)"
        cursor = db.cursor()
        try:
            cursor.execute(sql, [str(new_id), new_oid, user_info, items[i], int(amount[i])])
            db.commit()
            print("You have successfully create a order")
        except:
            db.rollback()
    showorders()
    print("=====end=====")
    main()

# def Order_cancel():
#     flag = 1
#     while flag:
#         user_info = input("Please enter your customer id:")
#         tag = show_user_orders(user_info)
#         if tag:
#             order_cancel = input("Which order you want to cancel:\n ")
#             item_cancel = input(
#                 "Which items you want to cancel in this order(if many oder you wwant cancel and each orderid with balank space):\n ")
#             willing_cancel_list = item_cancel.split()
#             for item in willing_cancel_list:
#                 sql = "DELETE FROM orders WHERE oid = %s AND cid = %s AND iid = %s"
#                 sql_2 = "UPDATE items SET quantity = quantity + 1 WHERE iid = %s"
#                 cursor = db.cursor()
#                 try:
#                     cursor.execute(sql, [int(order_cancel), int(user_info), int(item)])
#                     cursor.execute(sql_2, int(item))
#                     db.commit()
#                 except:
#                     db.rollback()
#         else:
#             print("Could not found your any orders ")
#         ans = int(input("Continue Cancelling: Yes:1 No:2\n"))
#         if ans == 2:
#             flag = 0
#     print("=====end=====")


def Order_cancel():
    user_info = input("Please enter your customer id:")
    tag = show_user_orders(user_info)
    if tag:
        cancel_tag = input("What you want to cancel? whole order:1 some items in order:2 :\n ")
        if int(cancel_tag) == 1:
            order_cancel = input("which order you want to cancel:")
            sql = "DELETE FROM orders WHERE oid = %s"
            cursor = db.cursor()
            try:
                cursor.execute(sql, order_cancel)
                db.commit()
                print("You have successfully cancelled the order")
            except:
                db.rollback()
        elif int(cancel_tag) == 2:
            end = True
            cancel_item_list = []
            while end:
                order_cancel = input("Input which id in order you want to cancel:")
                cancel_item_list.append(order_cancel)
                flag = input("Continue cancelling Yes:1 No:2")
                if int(flag) == 2:
                    end = False
            for cancel_id in order_cancel:
                sql = "DELETE FROM orders WHERE id = %s"
                cursor = db.cursor()
                try:
                    cursor.execute(sql, cancel_id)
                    db.commit()
                    print("You have successfully cancelled the items in order")
                except:
                    db.rollback()
        else:
            print("Unsuccessfully cancel due to the illeagal input")
    print("=====end=====")
    main()

def conclude():
    db.close()


if __name__ == '__main__':
    main()