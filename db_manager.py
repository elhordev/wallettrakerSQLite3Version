import pandas as pd
import sqlite3
import os


def create_db():
    if os.path.exists('./db/user.db'):
        pass
    else:
        os.mkdir('./db')
        user_conn = sqlite3.connect('./db/user.db')
        cursor = user_conn.cursor()
        user_conn.execute("""
                    CREATE TABLE IF NOT EXISTS user (
                    id integer primary key autoincrement,
                    name text(255)
                    )
                    """)
        user_conn.close()


def choose_user():
    
    try:
        user_conn = sqlite3.connect('./db/user.db')
        user_df = pd.read_sql('SELECT * FROM user',user_conn,)
        user_df = user_df.reset_index(drop=True)
        user_df = user_df.set_index('id')
        print(user_df)
    except sqlite3.OperationalError:
        print('No existen usuarios.')

    user_id = input('Cual es tu usuario?\n'
                    '[A]Crear Nuevo Usuario\n'
                    '[Q]Salir\n')
    if user_id == 'A' or user_id == 'a':
       
        try:
            new_user_name = input('Cual es el nombre del nuevo usuario?\n')
            
            
            os.makedirs(f'./db/user/{new_user_name}')
            user_conn.execute("INSERT INTO user(name) VALUES (?)",(new_user_name,))
            user_conn.commit()
            user_conn.close()
            
            user_conn = sqlite3.connect(f'./db/user/{new_user_name}/stock_wallet_{new_user_name}.db')
            user_conn.execute(f"""
        CREATE TABLE stock_wallet_{new_user_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock TEXT(255),
        buy_price REAL,
        taxes REAL,
        date TEXT(255),
        qty INTEGER,
        accountcharge REAL
        )
        """)
            user_conn.close()

            user_conn = sqlite3.connect(f'./db/user/{new_user_name}/stock_sales_{new_user_name}.db')
            user_conn.execute(f"""
        CREATE TABLE stock_sales_{new_user_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock TEXT(255),
        sell_price REAL,
        taxes REAL,
        date TEXT(255),
        qty INTEGER,
        accountincome REAL
        )
        """)
            user_conn.close()
        except FileExistsError:
            print('Usuario existente, por favor, elija otro nombre de usuario')
            choose_user()


    if user_id == 'Q' or user_id == 'q':
        exit()