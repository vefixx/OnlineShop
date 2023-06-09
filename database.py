import sqlite3
import random
import string
conn = sqlite3.connect('shop.db', check_same_thread=False)

def check_login(login):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    data = cursor.fetchone()
    print(data)
    if data is not None:
        return True
    else:
        return False
    
def check_password(password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE password=?", (password,))
    data = cursor.fetchone()
    print(data)
    if data is not None:
        return True
    else:
        return False
    

def add_user(login, password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (login, password) VALUES (?,?)", (login, password))
    conn.commit()

def del_all():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shop")
    conn.commit()

def del_user(login):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE login = ? ", (login,))
    conn.commit()

def add_product(name, price, amount,image):
    cursor = conn.cursor()
    ready = False
    while ready != True:
        id = random.randint(0, 9999)
        cursor.execute("SELECT * FROM shop WHERE product_id = ?", (id,))
        data = cursor.fetchall()
        if data == []:
            cursor.execute('''INSERT INTO shop (product_name, price, amount, product_id, image_src) VALUES(?,?,?,?,?)''', (name, price, amount, id, image))
            ready = True
        else:
            print(id, 'none')
    conn.commit()
    return True

def del_product(name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shop WHERE product_name = ? OR product_id = ?", (name, name))
    conn.commit()


def get_product():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shop")
    data = cursor.fetchall()
    return data

def search_products(search_query):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM shop WHERE LOWER(product_name) LIKE ?", ('%' + search_query.lower() + '%',))

    data = cursor.fetchall()
    return data

def generate_secret_key(length):
    characters = string.ascii_letters + string.digits
    secret_key = ''.join(random.choice(characters) for _ in range(length))
    return secret_key

def add_product_more(name, price, amount,image):
    cursor = conn.cursor()
    for i in range(20):
        ready = False
        while ready != True:
            id = random.randint(0, 9999)
            cursor.execute("SELECT * FROM shop WHERE product_id = ?", (id,))
            data = cursor.fetchall()
            if data == []:
                cursor.execute('''INSERT INTO shop (product_name, price, amount, product_id, image_src) VALUES(?,?,?,?,?)''', (name, price, amount, id, image))
                ready = True
            else:
                print(id, 'none')
        conn.commit()
    return True


def add_product_in_cart(user_login, product_id, old_products):
    cursor = conn.cursor()
    if old_products:
        new_cart_products = str(old_products) + ',' + str(product_id)
    else:
        new_cart_products = str(product_id)
    cursor.execute("UPDATE users SET cart_products = ? WHERE login = ?", (new_cart_products, user_login))
    conn.commit()
    return True


def get_product_in_cart(user_login):
    cursor = conn.cursor()
    cursor.execute("SELECT cart_products FROM users WHERE login = ?", (user_login,))
    data = cursor.fetchone()[0]
    return data


def total_product_in_cart(products):
    if products:
        total = str(products).split(",")
    else:
        total = []
    return total

def get_amount_in_cart(cart):
    if cart:
        values_list = str(cart).split(",")
        count = len(values_list)
    else:
        count = 0
    return count

def main():
    #print(get_product())
    #print(search_products('Компьютер'))
    #print(add_product('product-test', 23900, 23, None))
    #print(add_product_in_cart('admin', 686, get_product_in_cart('admin')))
    print(total_product_in_cart(get_product_in_cart('admin')))
    print(get_amount_in_cart(get_product_in_cart('admin')))
    
    
    




if __name__ == '__main__':
    main()