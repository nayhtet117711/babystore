from flask import Flask, render_template, redirect, request, send_from_directory

import os

from route import index, product, product1, about

app = Flask(__name__)

app.add_url_rule("/", "index", index, methods=["GET", "POST"])

app.add_url_rule("/product/<ftype>/<fname>", "product", product, methods=["GET", "POST"])

app.add_url_rule("/product/<ftype>", "product2", product1, methods=["GET", "POST"])

app.add_url_rule("/about", "about", about   , methods=["GET", "POST"])

if __name__ == "__main__":
   app.run(debug=True)