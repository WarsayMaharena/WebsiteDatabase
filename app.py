from flask import Flask, render_template, request, redirect, url_for
from userdb import User

app = Flask(__name__)


@app.route('/shoppingbasket', methods=('GET','POST'))
def shoppingbasket():
    user = User()
    customerid = user.get_customerid()
    posts = user.fetch_items_shoppingbasket(customerid)
    message = user.calc_price(customerid)
    if request.method == 'POST':
        furnitureid = request.form.get('furnitureid')
        user.remove_item_shoppingbasket(furnitureid,customerid)
        return redirect(url_for('shoppingbasket', posts=posts, message=message))
    
    return render_template('shoppingbasket.html', posts=posts, message=message)


@app.route('/checkout', methods=('GET', 'POST'))
def checkout():
    user = User()
    if request.method == 'POST':
        card_number = request.form.get('card_number')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        cvc = request.form.get('cvc')
        card_month = request.form.get('card_month')
        card_year = request.form.get('card_year')
        city = request.form.get('city')
        customerid = int(user.get_customerid())
        user.add_card_credentials(card_number, customerid, first_name, cvc, card_month, card_year)
        user.place_order(customerid, last_name, first_name, city)
        #user.place_order_help(customerid)
        #user.remove_all_shoppingbasket(customerid)
        return redirect(url_for('placeorder'))

    return render_template('checkout.html')


@app.route('/placeorder')
def placeorder():
    user = User()
    return render_template('placeorder.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    user = User()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if (str(email) == 'admin@hotmail.com') and (str(password) == 'admin'):
            return redirect(url_for('adminhomepage'))
        elif user.authentication(email, password) == True:
            return redirect(url_for('homepage'))
        else:
            return "Email or password is incorrect"
        
    return render_template('login.html')


@app.route('/createaccount', methods=('GET', 'POST'))
def createaccount():
    user = User()
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        city = request.form.get('city')
        address = request.form.get('address')
        zip = request.form.get('zip')
        password = request.form.get('password')
        if user.check_email(email) == False:
            return "Email aldready exists"
        else:
            user.create_user(last_name, first_name, city, address, email, password)
            return redirect(url_for('homepage'))
    
    return render_template('createaccount.html')



@app.route('/', methods=('GET', 'POST'))
def homepage():
    user = User()
    posts = user.fetch_assets()
    customerid = user.get_customerid()
    if request.method == 'POST':
        price = request.form.get('price')
        furniture = str(request.form.get('furniture'))
        furnitureid = request.form.get('furnitureid')
        quantity = request.form.get('quantity')
        wantedquantity = request.form.get('wantedquantity')
        if (price == None) and (furnitureid != None):
            return redirect(url_for('comments', furnitureid=furnitureid))
        else:
            quantity = int(request.form.get('quantity'))
            wantedquantity = int(request.form.get('wantedquantity'))
            if(wantedquantity>quantity):
                return "Error: the stock is " +str(quantity) +" but you wanted a stock of "+ str(wantedquantity)
            if(user.alreadyAddedInCart(customerid,furnitureid)==True):
                return "The added item already exists in your cart"
            else:
                customerid = user.get_customerid()
                user.add_item_shoppingbasket(furniture, price, furnitureid, customerid, wantedquantity)
                user.quantity_vs_wantedquantity(quantity, wantedquantity,furnitureid)
                return redirect(url_for('homepage'))
            


    return render_template('homepage.html', posts=posts)



@app.route('/comments/<furnitureid>', methods=('GET', 'POST'))
def comments(furnitureid):
    user = User()
    posts = user.fetch_asset(furnitureid)
    comment = user.fetch_comments(furnitureid)
    if request.method == 'POST':
        c = str(request.form.get('comment'))
        grading = str(request.form.get('grading'))
        customerid = int(user.get_customerid())
        furnitureid = int(furnitureid)
        if(user.AvailableToComment(customerid,furnitureid)==True):
            user.comment_post(furnitureid, customerid, c, grading)
            user.calc_average_grading(furnitureid)
        return redirect(url_for('comments', furnitureid=furnitureid))

    return render_template('commentpage.html', posts=posts, comment=comment)



@app.route('/admin', methods=('GET','Post'))
def admin():
    user=User()
    posts=user.fetch_usercustomer()
    if request.method == 'POST':
        customerid = request.form.get('CustomerID')
        #user.remove_comment()
        if(user.delete_user(customerid)==False):
            return " you cannot delete admin"
        
        user.delete_user(customerid)

        
        return redirect(url_for('admin'))
    
    return render_template('admin.html', posts=posts)


@app.route('/adminhomepage', methods=('GET', 'POST'))
def adminhomepage():
    user = User()
    posts = user.fetch_assets()
    if request.method == 'POST':
        price = request.form.get('price')
        furniture = str(request.form.get('furniture'))
        furnitureid = request.form.get('furnitureid')
        quantity = request.form.get('quantity')
        Editbutton= request.form.get('Editbutton')
        if(Editbutton != None):
            return redirect(url_for('admineditpage', furnitureid=furnitureid))
        elif furnitureid != None:
            user.remove_asset(furnitureid)
            return redirect(url_for('adminhomepage'))
        else:   
            user.post_item(price, furniture, quantity)
            return redirect(url_for('adminhomepage'))
    return render_template('adminhomepage.html', posts=posts)


@app.route('/admineditpage/<furnitureid>', methods=('GET','POST'))
def admineditpage(furnitureid):
    user=User()
    posts=user.fetch_asset(furnitureid)
    if request.method == 'POST':
        price = str(request.form.get('price'))
        furniture = str(request.form.get('furniture'))
        quantity = str(request.form.get('quantity'))
        user.EditAsset(furnitureid,quantity,price,furniture)
        return redirect(url_for('adminhomepage'))



    return render_template('admineditpage.html', posts=posts)

@app.route('/adminorders', methods=('GET', 'POST'))
def adminorders():
    user = User()
    posts = user.fetch_orders()
    Orders = user.fetch_place_order_help()
    if request.method == 'POST':
        Cancelorder = int(request.form.get('Cancelorder'))
        user.QuantityReturned(Cancelorder)
        user.EditOrdersStatus(Cancelorder)
        return redirect(url_for('adminorders'))
    return render_template('adminorders.html', posts=posts, Orders=Orders)

app.run()

    
    

