from flask import Flask, render_template, request, make_response, send_from_directory, escape, redirect, url_for
import os
from os.path import splitext
import random
import datetime
from flask_mysqldb import MySQL
from baby_store1 import doTheory
from werkzeug import secure_filename

app = Flask(__name__)

mysql = MySQL(app)

class Item :
    no = 0
    type = ""
    fname = ""
    img = ""
    price = 0.0
    aprice = 0.0
    id = 0,
    promotion = False
    promoPercent=10 

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
        cursor = mysql.connection.cursor()
        cursor.execute("select distinct category from product")
        categoryList = [ c[0] for c in cursor.fetchall()]
        mysql.connection.commit()
        cursor.close()
        return render_template(
            'index.html',
            itemList = itemList,
            categoryList=categoryList,
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

    cursor = mysql.connection.cursor()
    cursor.execute("select items from bill")
    fetchedBillData = cursor.fetchall()

    recomProduct2 = []
    for it1 in searchProducts:
        recomProduct2.append(it1)
        doit = False
        for it2 in recommendatedProducts:
            for bl in fetchedBillData:
                count1 = 0
                count2 = 0
                # print(" ||======================")
                for c in bl[0].split("_-_") :                        
                    pitem = c.split(",")
                    idd = int(pitem[0])
                    # if (idd==str(1)) | (idd==str(373)) :
                    #     print("idd: ", idd, "  <> item1: ", it1.id, " <> item2: ", it2.id)
                    
                    if it1.id==idd:
                        count1 += 1
                    if it2.id==idd:
                        count2 += 1

                if (count1>0) & (count2>0):
                    it2.promotion = True
                    recomProduct2.append(it2)
                    doit = True
                    break
                    # print( "item1: ", it1.id, it1.promotion, " <<>> item2: ", it2.id, it2.promotion)            
        if not doit :
            recomProduct2.append(None)
        
    # print("recomProduct2: ", recomProduct2)


    return render_template(
        'product.html',
        item = item,
        searchProducts = searchProducts,
        # itemList = recommendatedProducts,
        itemList = recomProduct2
    )

def saveProduct() :
    name = request.form['name']
    price = request.form['price']
    category = request.form['category']
    img = request.files['img']
    
    imgFileName = secure_filename(img.filename)
    img.save(os.path.join(app.root_path, 'static', "photos", category, imgFileName))

    cursor = mysql.connection.cursor()
    cursor.execute("insert into product(name, category, price, img) values(%s, %s, %s, %s)", (name, category, price, img.filename))
    mysql.connection.commit()
    cursor.close()

    return redirect("/?newProduct=1")

def addToCart(itemId, prevUrl) : 
    loggedName = request.cookies.get("loggedName")
    if not loggedName:
        return redirect("/login")

    itemList, fileTypeList = readProducts(mysql)
    item = Item()
    for item1 in itemList:
        if int(item1.id)==int(itemId):
            item.id = item1.id
            item.price = item1.price
            item.fname = item1.fname
            item.type = item1.type
            item.img = item1.img
            break
    itemString = str(item.id)+","+str(item.fname)+","+str(item.type)+","+str(item.price)
    cart = str(request.cookies.get("cart"))
    if cart=="":
        cart = itemString
    else :
        cart = cart + "_-_" + itemString

    cartCount = len(cart.split("_-_"))
    # for c in cart.split(" "):
    #     pitem = c.split(",")
    #     print(pitem)

    response = make_response(redirect(prevUrl.replace("$", "/")))
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
    # print("cc::", cart)
    for c in cart.split("_-_"):
        pitem = c.split(",")
        itemCount += 1
        it = Item()
        it.id = pitem[0]
        it.fname = pitem[1]
        it.type = pitem[2]
        it.price = pitem[3]
        it.no = itemCount
        itemList.append(it)

    cursor = mysql.connection.cursor()
    cursor.execute("select items from bill")
    fetchedData = cursor.fetchall()

    for i in range(0, len(itemList)):
        for k in range(0, len(itemList)):
            # itemList[i] = itemList[i]
            # itemList[k] = itemList[k]
            # print(len(itemList),i, k)
            if itemList[i].id!=itemList[k].id:
                for bl in fetchedData:
                    count1 = 0
                    count2 = 0
                    # print(" ||======================")
                    for c in bl[0].split("_-_") :                        
                        pitem = c.split(",")
                        idd = pitem[0]
                        
                        if itemList[i].id==idd:
                            count1 += 1
                        if itemList[k].id==idd:
                            count2 += 1

                        # print( itemList[i].id, itemList[i].fname, itemList[k].id, itemList[k].fname, idd, pitem[1])
                    if (count1>0) & (count2>0):
                        itemList[i].promotion = True
                        itemList[k].promotion = True

    for it in itemList:
        # print(it.fname, it.promotion)
        if it.promotion:
            it.aprice = float(it.price) * 0.9
        else :
            it.aprice = float(it.price)
        totalAmount += float(it.aprice)   

    mysql.connection.commit()
    cursor.close()

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
    for c in cart.split("_-_"):
        pitem = c.split(",")
        itemCount += 1
        it = Item()
        it.id = pitem[0]
        it.fname = pitem[1]
        it.type = pitem[2]
        it.price = pitem[3]
        it.no = itemCount
        totalAmount += float(it.price)
        itemList.append(it)
    
    cursor = mysql.connection.cursor()
    cursor.execute("insert into bill(items, totalAmount, email, date) values(%s, %s, %s, %s)", (cart, totalAmount, loggedEmail, datetime.datetime.now()))
    mysql.connection.commit()
    cursor.close()

    response = make_response(redirect("/"))
    response.set_cookie("cart", "")
    response.set_cookie("cartCount", "")

    return response

def clearCart() :
    loggedName = request.cookies.get("loggedName")
    loggedEmail = request.cookies.get("loggedEmail")
    if not loggedName:
        return redirect("/login")
    
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