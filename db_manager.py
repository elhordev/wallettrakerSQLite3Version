import pandas as pd
import sqlite3

def choose_user():
    user_conn = sqlite3.connect('./db/user.db')
    user_df = pd.read_sql('SELECT * FROM user',user_conn,)
    user_df = user_df.reset_index(drop=True)
    user_df = user_df.set_index('id')
    print(user_df)
        
    user_id = input('Cual es tu usuario?\n'
                    '[A]Crear Nuevo Usuario\n'
                    '[Q]Salir\n')
    if user_id == 'A' or user_id == 'a':
        new_user_name = input('Cual es el nombre del nuevo usuario?\n')
        user_conn.execute("INSERT INTO user(name) VALUES (?)",(new_user_name,))
        user_conn.commit()
        user_conn.close()
    if user_id == 'Q' or user_id == 'q':
        exit()