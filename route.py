from flask import Flask, render_template, request, send_from_directory, escape

import os

from baby_store1 import doTheory

class Item :
    type = ""
    fname = ""

photoDirlist = os.listdir("static/photos")
product_list = []
ftype_list = []

for photo in photoDirlist:
    photo_list = os.listdir("static/photos/"+photo)
    for item in photo_list :
        d = Item()
        d.type = photo
        d.fname = item
        product_list.append(d)
        ftype_list.append(d.type)

match_list = doTheory()

def index() :
    return render_template(
        'index.html',
        itemList = product_list,
        type_list = list(dict.fromkeys(ftype_list))
        )

def product1(ftype) :
    return product(ftype, "")

def product(ftype, fname) :
    item = Item()
    item.type = ftype
    item.fname = fname

    tmp1 = []
    for match in match_list :
        for match1 in match :
            if match1.lower()==ftype.lower() :
                for tmp2 in match: 
                    if tmp2.lower()!=ftype.lower() : 
                        tmp1.append(tmp2)
        
    matched_item_types = list(dict.fromkeys(tmp1))
    print(matched_item_types)

    recommendatedProducts = []
    for item_type in matched_item_types :
        for product in product_list:
            if item_type.lower()==product.type.lower() :
                recommendatedProducts.append(product)
    
    searchProducts = []
    for product in product_list:
        if (ftype.lower()==product.type.lower()) & (len(searchProducts)<15) :
            searchProducts.append(product)

    return render_template(
        'product.html',
        item = item,
        searchProducts = searchProducts,
        itemList = recommendatedProducts
    )

def about() :
    return render_template(
        'about.html',
        )
