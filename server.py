from flask import Flask, render_template, redirect, request, send_from_directory
import os
from route import index, product, product1, about, signup, login, logout, addToCart, cart, checkOutCart, saveProduct, clearCart

app = Flask(__name__)

app.config.setdefault('MYSQL_HOST', 'localhost')
app.config.setdefault('MYSQL_USER', "user125")
app.config.setdefault('MYSQL_PASSWORD', "root")
app.config.setdefault('MYSQL_DB', "babystoredb")
app.config.setdefault('MYSQL_PORT', 3306)
app.config.setdefault('MYSQL_UNIX_SOCKET', None)
app.config.setdefault('MYSQL_CONNECT_TIMEOUT', 10)
app.config.setdefault('MYSQL_READ_DEFAULT_FILE', None)
app.config.setdefault('MYSQL_USE_UNICODE', True)
app.config.setdefault('MYSQL_CHARSET', 'utf8')
app.config.setdefault('MYSQL_SQL_MODE', None)
app.config.setdefault('MYSQL_CURSORCLASS', None)

app.add_url_rule("/", "index", index, methods=["GET", "POST"])

app.add_url_rule("/product/<ftype>/<fname>", "product", product, methods=["GET", "POST"])

app.add_url_rule("/product/<ftype>", "product2", product1, methods=["GET", "POST"])

app.add_url_rule("/about", "about", about   , methods=["GET", "POST"])

app.add_url_rule("/saveProduct", "saveProduct", saveProduct   , methods=["POST"])

app.add_url_rule("/signup", "signup", signup   , methods=["GET", "POST"])

app.add_url_rule("/login", "login", login   , methods=["GET", "POST"])

app.add_url_rule("/logout", "logout", logout   , methods=["GET", "POST"])

app.add_url_rule("/add-to-cart/<itemId>/<promotion>/<rootType>/<prevUrl>", "add-to-cart", addToCart   , methods=["GET", "POST"])

app.add_url_rule("/cart", "cart", cart   , methods=["GET", "POST"])

app.add_url_rule("/clearCart", "clearCart", clearCart   , methods=["GET", "POST"])

app.add_url_rule("/cart-checkout", "cart-checkout", checkOutCart   , methods=["GET", "POST"])


if __name__ == "__main__":
   app.run(debug=True)