import sqlite3
from random import randint
conn = sqlite3.connect('shop.db', check_same_thread=False)

oper = str(input('user/shop content: '))
q = str(input('add/del: '))

#вошли в операции с товарным ассортиментом
if oper.lower() == 'shop content':
    #операция добавления товара
    if q.lower() == 'add':
        cursor = conn.cursor()
        name = str(input('product name: '))
        price = str(input('product price: '))
        amount = str(input('product amount: '))
        image = str(input('Image name: (example.png): '))
        try:
            id = randint(1,9999)
            cursor.execute('''INSERT INTO shop (product_name, price, amount, product_id, image_src) VALUES(?,?,?,?,?)''', (name, price, amount, id, image))
            print(f'Successful added "{name}" with {id} id')
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()
        

    #операция с удалением товара из списка
    elif q.lower() == 'del':
        cursor = conn.cursor()
        name_for_delete = str(input('product name/product id: '))
        try:
            cursor.execute("DELETE FROM shop WHERE product_name = ? OR product_id = ?", (name_for_delete, name_for_delete))
            print(f'Successful delete "{name_for_delete}"')
        except Exception:
            print('The product was not found in the database.')
        conn.commit()
        conn.close()

#вход в операции с добавление или удалением пользователя  
if oper.lower() == 'user':
    #если добавляем
    if q.lower() == 'add':
        login = str(input('user login: '))
        password = str(input('user password: '))

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (login, password) VALUES(?,?)", (login, password))
            print(f'Successful added "{login}"')
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()
    #если удаляем
    elif q.lower() == 'del':
        login = str(input('login: '))
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE login = (?)", (login,))
            print(f'Successful delete "{login}"')
        except Exception as e:
            print(e)
            print('The user was not found in the database.')
        conn.commit()
        conn.close()

