'''
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
'''

import datetime
import time

from helpers import *

'''
# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """ display summary of user's current stock holdings """
    '''

    # identify user
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=user_id)
    username = username[0]["username"] # unpackage value
    
    # initialize date stamp
    timestamp = time.time()
    date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    # identify unique stock types in purchases
    stock_groups = db.execute("SELECT stock FROM purchases WHERE id = :user_id GROUP BY stock", user_id=user_id)
    
    # identify iterable range of values in stock_groups
    iterable_range = range(len(stock_groups))
    
    # look up current prices (returns dicts in list)
    look_up = []
    for i in iterable_range:
        item = (lookup(stock_groups[i]["stock"]))
        look_up.append(item)
        
    # append i'th quantities of stocks owened into qty_summary list
    qty_summary = []
    for i in iterable_range:
        # sum quantity of i'th stock in purchases
        p = db.execute("SELECT SUM(quantity) FROM purchases WHERE stock = :stock AND id = :user_id", stock = stock_groups[i]["stock"], user_id=user_id)
        p_sum=(p[0]["SUM(quantity)"]) # unpackage value
        
        # sum quantity of i'th stock in sales
        s = db.execute("SELECT SUM(quantity) FROM sales WHERE stock = :stock AND id = :user_id", stock = stock_groups[i]["stock"], user_id=user_id)
        s_sum=(s[0]["SUM(quantity)"]) # unpackage value
        if s_sum == None:
            s_sum = 0
        
        final_sum = p_sum - s_sum # subract quantity of sales from quantity of purchases
        qty_summary.append(final_sum)
    
    # evaluate current total worth per stock group (if stock not null)
    current_valuation = []
    for i in iterable_range:
        if qty_summary[i] != 0:
            final_sum = look_up[i]["price"] * qty_summary[i] # price per share x quantity owned
            current_valuation.append(final_sum) # append final sum to list
        else:
            current_valuation.append(None) # append list with None value if stock was null
            
    # return cash balance from users database
    cash_balance = db.execute("SELECT cash FROM users WHERE id= :user_id", user_id=user_id)
    cash_balance = cash_balance[0]["cash"] # unpackage value
    
    # sum current stock values (filtering None values)
    stock_balance = sum(filter(None, current_valuation))
    
    # total balance of cash and stock assets
    total_balance = stock_balance + cash_balance
    
    # render index page, submit variables to HTML
    return render_template("index.html", iterable_range=iterable_range, symbol=stock_groups, name=look_up, quantity=qty_summary, \
    currentvaluation=current_valuation, currentprice=look_up, username=username, cash_balance=usd(cash_balance), \
    total_balance=usd(total_balance), stock_balance=usd(stock_balance), sum=sum, usd=usd)

'''    
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    # if user reached route via GET
    if request.method == "GET":
        return render_template("buy.html") # render "buy" page
    
    # if user reached route via POST (as by form submission)
    if request.method == "POST":
        
        # remember user logged in
        user_id = session["user_id"]
'''

        # if no stock code provided, return re-prompt
        if not request.form.get("symbol"):
            return apology("please provide stock code")
        
        # if no quantity provided, return re-prompt    
        if not request.form.get("shares").isdigit():
           return apology("please provide quantity of shares")
        
        # if quantity is negative int, return re-prompt   
        quantity = int(request.form.get("shares"))
        if quantity < 1:
            return apology("quantity must be at least 1")
        
        # return cash balance of user
        user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        user_cash = user_cash[0]["cash"] # unpackage value
        
        # look up current valuation of stock
        look_up = lookup(request.form.get("symbol"))
        # if stock code provided is invalid, return re-prompt
        if look_up == None:
            return apology("invalid stock code, please try again")
        
        # evaluate total price
        total_price = quantity * look_up["price"]
        
        # initialize date stamp
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # if user does not have enough funds, return apology
        if user_cash < total_price:
            return apology("sorry, you do not have enough funds to complete this purchase")
        else:
            # if user has enough funds, subtract the purchase from user's cash balance and record to database
            user_cash -= total_price 
            db.execute("UPDATE users SET cash = :user_cash WHERE id = :user_id", user_cash=user_cash, user_id=user_id)
            db.execute("INSERT INTO purchases (id, date, stock, name, price, quantity, total) VALUES (:user_id, :date, :symbol, :name, :price, :quantity, :total)" \
            , user_id=user_id, date=date, symbol=look_up["symbol"], name=look_up["name"], price=look_up["price"], quantity=quantity, total=total_price)
            
            # purchase was successful, render summary page of transaction
            return render_template("bought.html", date=date, code=look_up["symbol"], name=look_up["name"], quantity=quantity, price=usd(look_up["price"]), total=usd(total_price))

'''    
@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
'''
    
    # remember user logged in
    user_id = session["user_id"]
    
    # from purchases table, return all user details
    purchases = db.execute("SELECT * FROM purchases WHERE id = :user_id", user_id=user_id)
    p_iterable_range = range(len(purchases)) # evaluate iterable range of "purchases"
    
    # from sales table, return all user details
    sales = db.execute("SELECT * FROM sales WHERE id = :user_id", user_id=user_id)
    s_iterable_range = range(len(sales)) # evaluate iterable range of "sales"
    
    # render history summary page, submitting variables to HTML
    return render_template("history.html", p_iterable_range=p_iterable_range, s_iterable_range=s_iterable_range, purchases=purchases, sales=sales, usd=usd)

'''
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
'''

    # clear previous session
    session.clear()

    # if user reached route via POST (as by form submission)
    if request.method == "POST":

        # ensure username is submitted, else re-prompt
        if not request.form.get("username"):
            return apology("please provide username")

        # ensure password is submitted, else re-prompt
        elif not request.form.get("password"):
            return apology("please provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct, else re-prompt
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["pwd_hash"]):
            return apology("invalid username and/or password")

        # remember user logged in
        session["user_id"] = rows[0]["id"]
        
        # redirect user to home page
        return redirect(url_for("index"))

    # if user reached route via GET, return login form
    else:
        return render_template("login.html")
'''
@app.route("/logout")
def logout():
    """Log user out."""

    # forget last log-in
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
'''
    
    # if user reached route via GET, return "quote" page
    if request.method == "GET":
       return render_template("quote.html")
     
    # if user reached route via POST (as by form submission)
    if request.method == "POST":
        
        # ensure stock code is submitted, else re-prompt
        if not request.form.get("symbol"):
            return apology("please provide a stock code")
        
        # ensure code is valid, else re-prompt
        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return apology("invalid stock code, please try again")
            
        # initialize date stamp
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # render quote summary page, submitting variables to HTML
        look_up = lookup(symbol)
        return render_template("quoted.html", name =look_up["name"], symbol=look_up["symbol"], price=usd(look_up["price"]), date=date)
'''
@app.route("/register", methods=["GET", "POST"])
def register():
    
    """Register user."""
'''
    
    # forget previous session
    session.clear()
    
    # if route is reached via GET request, direct to register page  
    if request.method == "GET":
        return render_template("register.html")
        
    # if route is reached via POST (as by form submission)
    if request.method == "POST":

        # ensure username was submitted, else re-prompt
        if not request.form.get("username"):
            return apology("please provide username")

        # ensure password was submitted, else re-prompt
        elif not request.form.get("password"):
            return apology("please provide password")
        
        # ensure password confirmation was submitted, else re-prompt
        elif not request.form.get("password confirmation"):
            return apology("please confirm password")
        
        # ensure username is not already taken, else re-prompt
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 0:
            return apology("User already exists, please enter a unique username")
        
        # ensure password and password confirmation match, else re-prompt
        if request.form.get("password") != request.form.get("password confirmation"):
            return apology("passwords do not match, please try again")
        else:
            pwd_hash = pwd_context.hash(request.form.get("password"))  # hash and remember password
            username = request.form.get("username")  # remember username
            
        # insert user details into database
        db.execute("INSERT INTO users (username, pwd_hash) VALUES (:username, :pwd_hash)", username=username, pwd_hash=pwd_hash)
        
        # log user in
        rows = db.execute("SELECT * FROM users WHERE username = :username AND pwd_hash = :pwd_hash", username=username, pwd_hash=pwd_hash)
        session["user_id"] = rows[0]["id"] # remember session

    # redirect user to index page
    return redirect(url_for("index"))

'''        
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
'''
    
    # identify user
    user_id = session["user_id"]
    
    # identify all unique stock types owned
    stock_groups = db.execute("SELECT stock FROM purchases WHERE id = :user_id GROUP BY stock", user_id=user_id)
    
    # identify iterable range of values returned in "stock_groups"
    iterable_range = range(len(stock_groups))
    
    #look up current valuation (dicts in list)
    look_up = []
    for i in iterable_range:
        item = (lookup(stock_groups[i]["stock"]))
        look_up.append(item) # append i'th look up into look_up list
        
    # sum quantity of shares for each unique stock type
    available_quantities = []
    for i in iterable_range:
        # return summed quantities of i'th stock from purchases
        p=db.execute("SELECT SUM(quantity) FROM purchases WHERE stock =:stock AND id =:user_id", stock=stock_groups[i]["stock"], user_id=user_id)
        p_quantity =p[0]["SUM(quantity)"] # unpackage value
        
        # return summed quantities of i'th stock from sales
        s = db.execute("SELECT SUM(quantity) FROM sales WHERE stock =:stock AND id =:user_id", stock=stock_groups[i]["stock"], user_id=user_id)
        s_quantity = s[0]["SUM(quantity)"] # unpackage value
        if s_quantity == None:
            s_quantity = 0
        
        # evaluate availability of stock for sale
        final = p_quantity - s_quantity
        available_quantities.append(final)
    
    # if route is reached via GET request, direct to sell page
    if request.method == "GET":
        return render_template("sell.html", iterable_range=iterable_range, symbol=look_up, name=look_up, quantity=available_quantities, currentvalue=look_up, \
        sum=sum, usd=usd)
    
    # if route is reached via POST request (form submission) 
    if request.method == "POST":
        
        # ensure stock symbol was submitted, else re-prompt
        if not request.form.get("symbol"):
            return apology("please provide stock code")
        
        # ensure stock is valid for sale by searching "stock_groups"
        symbol = (request.form.get("symbol")).upper()
        tracker = 0 # index
        for i in iterable_range:
            if symbol in stock_groups[i]["stock"]:
                break
            else:
                tracker += 1
                
        # if symbol not found in "stock_groups", re-prompt
        if tracker == len(iterable_range): 
            return apology("please provide valid stock code")
        
        # ensure quantity was submitted, else re-prompt
        if not request.form.get("shares").isdigit():
           return apology("please provide valid quantity of shares")
        
        # ensure quantity submitted is greater than 0, else re-prompt
        quantity = int(request.form.get("shares"))
        if quantity < 1:
            return apology("quantity must be at least 1")
        
        # ensure quantity requested is not greater than quantity available, else re-prompt
        available_quantity = available_quantities[tracker]
        print(available_quantities)
        if quantity > available_quantity:
            return apology("please enter a valid quantity to sell")
        else:
            
            # initialize date stamp
            timestamp = time.time()
            date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            # look up current valuation of stock
            look_up = lookup(symbol)
            
            # total price of sale
            sales_total = look_up["price"] * quantity
            
            # record sale in database
            db.execute("INSERT INTO sales (id, date, stock, name, price, quantity, total) VALUES (:user_id, :date, :symbol, :name, :price, :quantity, :total)" \
            , user_id=user_id, date=date, symbol=symbol, name=look_up["name"], price=look_up["price"], quantity=quantity, total=sales_total)
            
            # update user cash balance with profit from sale
            user_cash=db.execute("SELECT cash FROM users WHERE id =:user_id", user_id=user_id)
            new_total = user_cash[0]["cash"] + sales_total
            db.execute("UPDATE users SET cash =:cash WHERE id =:user_id", user_id=user_id, cash=new_total)
            
            # render sold summary page, submit variables to HTML
            return render_template("sold.html", date=date, code=symbol, name=look_up["name"], quantity=quantity, price=look_up["price"], total=sales_total, usd=usd)
            
@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    
    # identify user
    user_id = session["user_id"]
    
    # if route is reached via GET, direct to top up page
    if request.method == "GET":
        return render_template("topup.html")
    
    # if route is reached via POST (form submission)   
    if request.method == "POST":
        
        # if top up amount submitted is not a valid int
        if not request.form.get("topup").isdigit():
            return apology("please enter a valid top up amount")
        
        # cast top up submission to float
        top_up = float(request.form.get("topup"))
        
        # only accept top up amounts more than $1, else return re-prompt
        if top_up < 1.0:
            return apology("please enter a top amount of $1.00 or more")
        
        # return current cash balance of user    
        cash = db.execute("SELECT cash FROM users WHERE id =:user_id", user_id=user_id)
        
        # evaluate new cash balance
        new_cash = cash[0]["cash"] + top_up
        
        # update database with new cash balance
        db.execute("UPDATE users SET cash =:cash WHERE id =:user_id", cash=new_cash, user_id=user_id)
        
        # top up is successful, return summary page
        return render_template("toppedup.html", new_cash=new_cash, top_up=top_up, usd=usd)
