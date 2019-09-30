from flask import Flask, render_template, request, make_response, send_from_directory, escape, redirect, url_for
import os
import random
import datetime
from flask_mysqldb import MySQL
from baby_store1 import doTheory

app = Flask(__name__)

mysql = MySQL(app)

class Item :
    no = 0
    type = ""
    fname = ""
    img = ""
    price = 0.0
    id = 0,

# photoDirlist = os.listdir("static/photos")
# product_list = []
# ftype_list = []

# for photo in photoDirlist:
#     photo_list = os.listdir("static/photos/"+photo)
#     for item in photo_list :
#         # print(item.split(".")[0])

#         d = Item()
#         d.type = photo
#         d.fname = item
#         product_list.append(d)
#         ftype_list.append(d.type)

def readProducts(mysql)  :
    cursor = mysql.connection.cursor()
    cursor.execute("select id, name, category, img, price from product")
    productList = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    itemList = []
    fileTypeList = []
    for product in productList:
        d = Item()
        d.id = product[0]
        d.fname = product[1]
        d.type = product[2]
        d.img = product[3]
        d.price = product[4]
        itemList.append(d)
        fileTypeList.append(d.type)
    return itemList, fileTypeList

match_list = doTheory()

def index() :
    itemList, fileTypeList = readProducts(mysql)

    loggedName = request.cookies.get("loggedName")
    if not loggedName:
        return redirect("/login")
    else :
        return render_template(
            'index.html',
            itemList = itemList,
            type_list = list(dict.fromkeys(fileTypeList))
        )

def product1(ftype) :
    return product(ftype, "")

def product(ftype, fname) :

    itemList, fileTypeList = readProducts(mysql)

    loggedName = request.cookies.get("loggedName")
    if not loggedName:
        return redirect("/login")

    item = Item()
    item.type = ftype
    item.fname = fname

    for item1 in itemList:
        if (item1.fname==fname) & (item1.type==ftype):
            item.id = item1.id
            item.price = item1.price
            item.img = item1.img
            break
    
    tmp1 = []
    # match_list = doTheory(itemList)
    for match in match_list :
        for match1 in match :
            if match1.lower()==ftype.lower() :
                for tmp2 in match: 
                    if tmp2.lower()!=ftype.lower() : 
                        tmp1.append(tmp2)
        
    matched_item_types = list(dict.fromkeys(tmp1))
    # print(matched_item_types)

    recommendatedProducts = []
    for item_type in matched_item_types :
        for product in itemList:
            if item_type.lower()==product.type.lower() :
                recommendatedProducts.append(product)
    
    searchProducts = []
    for product in itemList:
        if (ftype.lower()==product.type.lower()) & (len(searchProducts)<15) :
            searchProducts.append(product)

    return render_template(
        'product.html',
        item = item,
        searchProducts = searchProducts,
        itemList = recommendatedProducts
    )

def addToCart(itemId) : 
    loggedName = request.cookies.get("loggedName")
    if not loggedName:
        return redirect("/login")

    itemList, fileTypeList = readProducts(mysql)
    item = Item()
    for item1 in itemList:
        if str(item1.id)==str(itemId):
            item.id = item1.id
            item.price = item1.price
            item.fname = item1.fname
            item.type = item1.type
            item.img = item1.img
            break
    itemString = str(item.id)+","+str(item.fname)+","+str(item.type)+","+str(item.price)
    cart = request.cookies.get("cart")
    if cart=="":
        cart = itemString
    else :
        cart = cart + " " + itemString

    cartCount = len(cart.split(" "))
    # for c in cart.split(" "):
    #     pitem = c.split(",")
    #     print(pitem)

    response = make_response(redirect("/"))
    response.set_cookie("cart", cart)
    response.set_cookie("cartCount", str(cartCount))
    
    return response

def cart() :
    loggedName = request.cookies.get("loggedName")
    if not loggedName:
        return redirect("/login")

    itemCount = 0
    itemList = []
    totalAmount = 0
    cart = request.cookies.get("cart")    
    for c in cart.split(" "):
        pitem = c.split(",")
        itemCount += 1
        it = Item()
        it.id = pitem[0]
        it.fname = pitem[1]
        it.type = pitem[2]
        it.price = pitem[3]
        it.no = itemCount
        totalAmount += int(it.price)
        itemList.append(it)


    return render_template(
        'cart.html',
        cartItemList = itemList,
        totalAmount = totalAmount
    )

def checkOutCart() :
    loggedName = request.cookies.get("loggedName")
    loggedEmail = request.cookies.get("loggedEmail")
    if not loggedName:
        return redirect("/login")

    itemCount = 0
    itemList = []
    totalAmount = 0
    cart = request.cookies.get("cart")    
    for c in cart.split(" "):
        pitem = c.split(",")
        itemCount += 1
        it = Item()
        it.id = pitem[0]
        it.fname = pitem[1]
        it.type = pitem[2]
        it.price = pitem[3]
        it.no = itemCount
        totalAmount += int(it.price)
        itemList.append(it)
    
    cursor = mysql.connection.cursor()
    cursor.execute("insert into bill(items, totalAmount, email, date) values(%s, %s, %s, %s)", (cart, totalAmount, loggedEmail, datetime.datetime.now()))
    mysql.connection.commit()
    cursor.close()

    response = make_response(redirect("/"))
    response.set_cookie("cart", "")
    response.set_cookie("cartCount", "")

    return response

def about() :
    return render_template(
        'about.html',
    )

def signup() :
    if request.method == 'GET':
        return render_template('signup.html')
    else :
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        # print(email, name, password)

        cursor = mysql.connection.cursor()
        cursor.execute("select email from user where email='%s'" % (email))
        email1 = cursor.fetchone()
        if(email1):
            return render_template('signup.html', errorText="Email already exists.")
        else:
            cursor.execute("insert into user(email, name, password) values(%s, %s, %s)", (email, name, password))
        mysql.connection.commit()
        cursor.close()
        return redirect("/login")

def login() :
    if request.method == 'GET':
        return render_template('login.html', **request.args)
    else :
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("select name from user where email='%s'" % (email))
        name = cursor.fetchone()
        if(name):
            response = make_response(redirect("/"))
            response.set_cookie("loggedEmail", email)
            response.set_cookie("loggedName", name[0])
            response.set_cookie("cart", "")
            response.set_cookie("cartCount", "")
            return response
        else :
            return redirect(url_for("login", errorText="Email or passord does not match!"))

def logout() :
    response = make_response(redirect("/"))
    response.set_cookie("loggedEmail", expires=0)
    response.set_cookie("loggedName", expires=0)
    response.set_cookie("cart", "", expires=0)
    response.set_cookie("cartCount", "", expires=0)
    return response