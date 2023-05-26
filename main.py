from flask import Flask, render_template, request, url_for, redirect, session, sessions
from database import *
from config import *
import string

app = Flask(__name__, static_folder='static')
app.secret_key = SECRET_KEY

knopka_admin = False
user_login = ''

@app.route('/', methods=['GET', 'POST'])
def default():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'is_authenticated' in session and session['is_authenticated']:
        return redirect('/main')
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        print(login, password)
        if check_login(login) and check_password(password):
            session['is_authenticated'] = True
            session['username'] = str(login)
            return redirect('/main')
        else:
            error_message = 'Invalid login or password'
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if 'is_authenticated' in session and session['is_authenticated']:
        return redirect('/main')
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if check_login(login):
            error_message = 'You already have an account'
            return render_template('register.html', error_message=error_message)
        else:
            add_user(login, password)
            return redirect('/login')
    return render_template('register.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if 'is_authenticated' not in session or not session['is_authenticated']:
        return redirect('/login')
    if 'is_authenticated' in session and session['is_authenticated']:
        if 'username' in session and session['username'] == 'admin':  
            print(session['username'])
            if request.method == 'POST':
                if 'add-product' in request.form:
                    name = request.form['product-name']
                    price = request.form['product-price']
                    amount = request.form['product-amount']
                    image = request.form['product-image']
                    add_product(name=name, price=price, amount=amount, image=image)
                    print('Add product')

                elif 'add-product+3' in request.form:
                    name = request.form['product-name']
                    price = request.form['product-price']
                    amount = request.form['product-amount']
                    image = request.form['product-image']
                    for i in range(3):
                        add_product(name=name, price=price, amount=amount, image=image)
                    print('Ready x3')

                elif 'add-product-more' in request.form:
                    for i in range(20):
                        name = generate_secret_key(5)
                        price = generate_secret_key(3)
                        amount = generate_secret_key(4)
                        image = None
                        add_product(name=name, price=price, amount=amount, image=image)
                    print('Ready more')
                
                elif 'del-product' in request.form:
                    name = request.form['product-name-id']
                    del_product(name)
                    print('del product')

                elif 'add-user' in request.form:
                    login = request.form['user-login']
                    password = request.form['user-password']
                    add_user(login, password)
                    print('Add user')

                elif 'del-user' in request.form:
                    login = request.form['user-login-del']
                    del_user(login)
                    print('del user')

                elif 'del-all' in request.form:
                    del_all()
                    print('del all shop')

                print('Ready')
        else:
            return redirect('/main')
    return render_template('admin.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'is_authenticated' in session and session['is_authenticated']:
        user_login = str(session['username'])
        cart = get_product_in_cart(user_login) #корзина юзера не чистым списком
        cart = total_product_in_cart(cart) #корзина юзера списком чистым списком
        products = get_product() #все продукты
        product_name = get_name_product_cart(cart) #продукты которые в корзине
        amount_cart = get_amount_cart_2(product_name) #количество товаров в корзине юзера
        if 'username' in session and session['username'] == 'admin':
            knopka_admin = True
            return render_template('shop.html', products=products, admin = knopka_admin, user_login = user_login, cart = amount_cart)        
        else:
            return render_template('shop.html', products=products, user_login = user_login, cart = amount_cart)
        
    else:
        return redirect('/login')
    


@app.route('/search', methods = ['GET', 'POST'])
def search():
    if 'is_authenticated' in session and session['is_authenticated']:
        if 'username' in session and session['username'] == 'admin':
            knopka_admin = True
        search = request.form['search']
        products = search_products(search)
        cart = get_product_in_cart(user_login) #корзина юзера не чистым списком
        cart = total_product_in_cart(cart) #корзина юзера списком чистым списком

        amount_cart = get_amount_in_cart(cart) #количество товаров в корзине юзера
        return render_template('search.html', products=products, admin = knopka_admin, user_login = user_login, cart = amount_cart)
    else:
        return redirect('/login')
    


@app.route('/delete/<int:product_id>', methods = ['GET', 'POST'])
def delete(product_id):
    if 'is_authenticated' in session and session['is_authenticated']:
        if 'username' in session and session['username'] == 'admin':  
            del_product(product_id)
            return redirect('/main')
        else:
            return redirect('/main')

@app.route('/addcart/<int:product_id>', methods=['GET', 'POST'])
def addcart(product_id):
    if 'is_authenticated' in session and session['is_authenticated']:
        user_login = session['username']  # Получение значения user_login из сессии
        old_products = get_product_in_cart(user_login)
        print(old_products)
        print(product_id)
        print(user_login)
        print(add_product_in_cart(user_login, product_id, old_products))
        

    return redirect('/main')



@app.route('/redirect', methods=['POST'])
def redirect_to_url():
    redirect_url = request.form['redirect_url']
    return redirect(redirect_url)
 
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'is_authenticated' in session and session['is_authenticated']:
        user_login = str(session['username'])
        cart = get_product_in_cart(user_login) #корзина юзера не чистым списком
        cart = total_product_in_cart(cart) #корзина юзера списком чистым списком
        products = get_name_product_cart(cart)
        amount_cart = get_amount_cart_2(products) #количество товаров в корзине юзера
        print(cart, amount_cart)
        if 'username' in session and session['username'] == 'admin':
            knopka_admin = True     
            return render_template('cart.html', products=products, admin = knopka_admin, user_login = user_login, cart = amount_cart)        
        else:
            return render_template('cart.html', products=products, user_login = user_login, cart = amount_cart)
        
    else:
        return redirect('/login')


if __name__ == '__main__':
   app.run(debug=True)