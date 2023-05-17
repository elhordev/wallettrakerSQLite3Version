from wallettraker_srcs import os, sqlite3, time, pd, wallet_at_use, datetime, main

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
        "index" INTEGER,
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
            choose_user()
        except FileExistsError:
            print('Usuario existente, por favor, elija otro nombre de usuario')
            choose_user()


    if user_id == 'Q' or user_id == 'q':
        exit()


    else:
        wallet_at_use = user_id
        return wallet_at_use
    
def add_to_wallet(realtime,wallet_at_use,borrado):
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()      
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    user_conn.close()
    print(user_at_use)
   
    df_acciones = pd.DataFrame(realtime)
    print(df_acciones)
    try:
        
        opcion = int(input("Qué valor del Ibex 35 has comprado?\n"))
                
               

        Stock = realtime[opcion]["Stock"]
        Buyprice = float(input(f"A que precio has comprado las acciones de {Stock} ?\n"))
        Qty = int(input(f"Cuantas acciones de {Stock} has comrpado a {Buyprice}?\n"))
        date_buy = "12/05/2023"
        Expense = float(input("Cuanto te han cobrado de gastos de compra?\n"))
        Index = opcion
        AccountCharge = (Buyprice * Qty) + Expense
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
        cursor = user_conn.cursor()
        cursor.execute(f'''INSERT INTO stock_wallet_{user_at_use} (stock,buy_price,taxes,date,qty,"index",accountcharge)
                          VALUES ('{Stock}',{Buyprice},{Expense},'{date_buy}',{Qty},{Index},{AccountCharge})
                          ''')
       
        user_conn.commit()
        cursor.close()
        user_conn.close()
        os.system(borrado)
        print(f"Añadida la compra de {Qty} acciones de {Stock} por un cargo en cuenta de {AccountCharge} euros.")
        
    except ValueError:
            os.system(borrado)
            print("Valor introducido incorrecto, solo valor numerico.")
            time.sleep(5)
            os.system(borrado)
            add_to_wallet(realtime,wallet_at_use,borrado)
    except IndexError:
            os.system(borrado)
            print(f"El Indice introducido se ha salido del rango, por favor , elije del 0 al {len(realtime)-1}.")
            time.sleep(5)
            os.system(borrado)
            add_to_wallet(realtime,wallet_at_use,borrado)
    time.sleep(5)
    os.system(borrado)
    
def db_manager_menu():
    option = input('¿Qué desea hacer con su Wallet?\n'
                   '[A]Añadir compra a la cartera.\n'
                   '[B]Añadir venta de la cartera.\n'
                   '[C]Eliminar compra de la cartera.\n'
                   '[D]Eliminar venta de la cartera.\n'
                   '[E]Modificar compra de la cartera.\n'
                   '[F]Modificar venta de la cartera.\n'
                   '[G]Buscar compra en la cartera.\n'
                   '[H]Buscar venta en la cartera.\n'
                   '[I]Ver cartera actual\n'
                   '[J]Ver ventas efectuadas.\n'
                   '[K]Volver atrás.')
    
    """if option == 'A' or option == 'a':
        add_to_wallet()
    
    if option == 'B' or option == 'b':
        #funcion para efectuar venta
    
    if option == 'C' or option == 'c':
        #funcion para eliminar compra por error
    if option == 'D' or option == 'd':
        #funcion para eliminar venta por error
    if option == 'E' or option == 'e':
        #funcion para modificar compra de la cartera por error
    if option == 'F' or option == 'f':
        #funcion para modificar venta de la cartera por error
    if option == 'G' or option == 'g':
        #funcion para buscar compra en la cartera
    if option == 'H' or option == 'h':
        #funcion para buscar venta en la cartera
    if option == 'I' or option == 'i':
        #funcion para ver cartera
    if option == 'J' or option =='j':
        #funcion para ver ventas
    if option == 'K' or option == 'k':
        main.main_menu()"""