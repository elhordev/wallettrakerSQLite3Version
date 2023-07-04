from wallettraker_srcs import os, sqlite3, time, pd, datetime, shutil
from main import main,main_menu,borrado_dep_so as borrado, wallet_at_use




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
                    '[A]Crear nuevo usuario\n'
                    '[B]Eliminar usuario existente\n'
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
        id_buy INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id_sale INTEGER PRIMARY KEY AUTOINCREMENT,
        id_buy INTEGER,
        stock TEXT(255),
        sell_price REAL,
        taxes REAL,
        date TEXT(255),
        qty INTEGER,
        accountincome REAL,
        foreign key(id_buy) references stock_wallet_{new_user_name}(id_buy)
        )
        """)
            user_conn.close()

           
            user_conn = sqlite3.connect(f'./db/user/{new_user_name}/balances_{new_user_name}.db')
            user_conn.execute(f"""
        CREATE TABLE balances_{new_user_name} (
        id_balance INTEGER PRIMARY KEY AUTOINCREMENT,
        id_buy INTEGER,
        stock TEXT(255),
        buy_price REAL,
        sell_price REAL,
        total_taxes REAL,
        date_buy TEXT(255),
        date_sell TEXT(255),
        qty INTEGER,
        balance REAL,
        foreign key(id_buy) references stock_wallet_{new_user_name}(id_buy),
        foreign key(buy_price) references stock_wallet_{new_user_name}(buy_price),
        foreign key(sell_price) references stock_sales_{new_user_name}(sell_price),
        foreign key(date_buy) references stock_wallet{new_user_name}(date),
        foreign key(date_sell) references stock_sales_{new_user_name}(date),
        foreign key(qty) references stock_sales_{new_user_name}(qty)
        )
        """)
            user_conn.close()        
               
            
            
            
            choose_user()
        except FileExistsError:
            print('Usuario existente, por favor, elija otro nombre de usuario')
            choose_user()

    if user_id == 'B' or user_id == 'b':
        print(user_df)
        opcion = int(input('¿Qué usuario quieres eliminar?'))
        user_conn = sqlite3.connect('./db/user.db')
        cursor = user_conn.cursor()      
        cursor.execute(f'SELECT * FROM user WHERE id={opcion}')
        user_to_delete = cursor.fetchone()
        user_to_delete = user_to_delete[1]
        cursor.execute(f'DELETE from user WHERE id={opcion}')
        cursor.close()
        user_conn.commit()
        user_conn.close()
        shutil.rmtree(f'./db/user/{user_to_delete}')
        print(f'Usuario {user_to_delete} eliminado, a chuparla!')
        time.sleep(2)
        os.system(borrado)
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
        date_buy = datetime.date.today()
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
        time.sleep(3)
        db_manager_menu(realtime,wallet_at_use,borrado)
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

def add_a_sell(realtime,wallet_at_use,borrado):
    
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    #Hemos seleccionado el usuario, viendo lo que se repite, hare una funcion a parte para esto.
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
    buy_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn,)
    buy_df = buy_df.reset_index(drop=True)
    buy_df = buy_df.set_index('id_buy')
    print(buy_df)

    #Imprimimos por df la tabla de las compras usando Pandas como consultor.
    cursor = user_conn.cursor()
    id_buy = int(input('A que compra pertenece esta venta?\n'))
    cursor.execute(f'SELECT stock FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
    stock = cursor.fetchone()
    #Si coincide el id introducido con un valor en la tabla de compras...
    if stock:
        stock = stock[0]
        cursor.execute(f'SELECT qty FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
        qty = cursor.fetchone()
        qty = qty[0]
        cursor.close()
        user_conn.close()
        sell_price = float(input('A que precio has vendido?\n'))
        taxes = float(input('Cuanto te han cobrado de tasas?\n'))
        accountincome = (sell_price * qty) - taxes
        date = datetime.date.today()
        
        while True:
            
            print(f'''\n
            Precio de venta {sell_price}\n
            Cantidad {qty}\n
            Tasas {taxes}\n
            Ingreso en cuenta {accountincome}\n
            Fecha {date},\n''')
            
            consulta = input('Los datos son correctos?[S\\N]\n')
            if consulta == 's' or consulta == 'S':

                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
                cursor = user_conn.cursor()
                cursor.execute(f'''INSERT INTO stock_sales_{user_at_use}(id_buy, stock, sell_price, taxes, date, qty,accountincome)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''',(id_buy,stock,sell_price,taxes,date,qty,accountincome,))
                user_conn.commit()
                cursor.close()
                user_conn.close()
                #Al cerrar la compra, agregamos el resultado a la tabla de balances.
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
                cursor = user_conn.cursor()
                #Importamos precio de compra
                cursor.execute(f'SELECT buy_price FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
                buy_price = cursor.fetchone()
                buy_price = buy_price[0]
                #Importamos taxes de la compra para poder sumarlo al total_taxes de la tabla balances.
                cursor.execute(f'SELECT taxes FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
                buy_taxes = cursor.fetchone()
                buy_taxes = buy_taxes[0]
                total_taxes = buy_taxes + taxes
                #Importamos la fecha de compra .
                cursor.execute(f'SELECT date FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
                date_buy = cursor.fetchone()
                date_buy = date_buy[0]
                #Calculamos el balance total
                cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
                buy_charge = cursor.fetchone()
                buy_charge = buy_charge[0]
                balance = accountincome - buy_charge
                cursor.close()
                user_conn.close()
                #Conectamos a la db de Balances.
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
                cursor = user_conn.cursor()
                cursor.execute(f'''INSERT INTO balances_{user_at_use}(id_buy, stock, buy_price, sell_price, total_taxes, date_buy, date_sell, qty, balance)
                                    VALUES(? ,?, ?, ?, ?, ?, ?, ?, ?)''',(id_buy,stock,buy_price,sell_price,total_taxes,date_buy,date,qty,balance))
                user_conn.commit()
                cursor.close()
                user_conn.close()
                            
                break
                
            if consulta == 'n' or consulta == 'N':
                print('Volvemos atras...')
                time.sleep(3)
                os.system(borrado)
                add_a_sell(realtime,wallet_at_use,borrado)
                break

            else:
                print('Selecciona la opcion correcta')

    

    
    
    else:
        print('Compra no encontrada, por favor, seleccione otra compra.')
        db_manager_menu(realtime,wallet_at_use,borrado)

def delete_a_buy(realtime,wallet_at_use,borrado):
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    #Hemos seleccionado el usuario, viendo lo que se repite, hare una funcion a parte para esto.
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
    buy_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn,)
    buy_df = buy_df.reset_index(drop=True)
    buy_df = buy_df.set_index('id_buy')
    print(buy_df)

    #Imprimimos por df la tabla de las compras usando Pandas como consultor.Tambien deberia de hacer una funcion para esto.
    #Still learning!
    cursor = user_conn.cursor()
    id_buy = int(input('Que compra deseas eliminar?\n'
                       '[A]Para ir atras.'))
    
    if id_buy == 'a' or id_buy == 'A':
        db_manager_menu(realtime,wallet_at_use,borrado)

    else:
                 
        cursor.execute(f'DELETE FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')
        user_conn.commit()
        rows_affected = cursor.rowcount
        if rows_affected == 0:
                print('El id_buy proporcionado no existe en la base de datos.')
                time.sleep(3)
                delete_a_buy(realtime,wallet_at_use,borrado)
        else:
                os.system(borrado)
                print('Compra eliminada satisfactoriamente.')
                time.sleep(3)
                cursor.close()
                user_conn.close()
                db_manager_menu(realtime,wallet_at_use,borrado)
        
        cursor.close()
        user_conn.close()
        os.system(borrado)
      
def delete_a_sell(realtime,wallet_at_use,borrado):
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    #Hemos seleccionado el usuario, viendo lo que se repite, hare una funcion a parte para esto.
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
    sell_df = pd.read_sql(f'SELECT * FROM stock_sales_{user_at_use}',user_conn,)
    sell_df = sell_df.reset_index(drop=True)
    sell_df = sell_df.set_index('id_sale')
    print(sell_df)

    #Imprimimos por df la tabla de las compras usando Pandas como consultor.Tambien deberia de hacer una funcion para esto.
    #Still learning!
    cursor = user_conn.cursor()
    id_sell = int(input('Que venta deseas eliminar?\n'
                       '[A]Para ir atras.'))
    
    if id_sell == 'a' or id_sell == 'A':
        db_manager_menu(realtime,wallet_at_use,borrado)           
    else:
        cursor.execute(f'SELECT id_buy FROM stock_sales_{user_at_use} WHERE id_sale = {id_sell}')
        delete_from_balances = cursor.fetchone()
        delete_from_balances = delete_from_balances[0]
        cursor.execute(f'DELETE FROM stock_sales_{user_at_use} WHERE id_sale = {id_sell}')
        user_conn.commit()
        rows_affected = cursor.rowcount
        if rows_affected == 0:
                print('El id_sell proporcionado no existe en la base de datos.')
                time.sleep(3)
                delete_a_sell(realtime,wallet_at_use,borrado)
        else:
                os.system(borrado)
                print('Compra eliminada satisfactoriamente.')
                cursor.close()
                user_conn.close()

                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
                cursor = user_conn.cursor()
                cursor.execute(f'DELETE FROM balances_{user_at_use} WHERE id_buy = {delete_from_balances}')
                user_conn.commit()
                cursor.close()
                user_conn.close()

                time.sleep(3)
                db_manager_menu(realtime,wallet_at_use,borrado)
        
        cursor.close()
        user_conn.close()
        os.system(borrado)

def modify_a_buy(realtime,wallet_at_use,borrado):
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    #Hemos seleccionado el usuario, viendo lo que se repite, hare una funcion a parte para esto.
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
    sell_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn,)
    sell_df = sell_df.reset_index(drop=True)
    sell_df = sell_df.set_index('id_buy')
    print(sell_df)

    #Imprimimos por df la tabla de las compras usando Pandas como consultor.Tambien deberia de hacer una funcion para esto.
    #Still learning!
    cursor = user_conn.cursor()
    id_sell = int(input('Que compra deseas modificar?\n'
                       '[A]Para ir atras.'))
    cursor.execute(f'SELECT id_buy FROM stock_wallet_{user_at_use}')
    num_registros = cursor.fetchall()

    if id_sell not in num_registros[0]:
        print('Compra  no encontrada, introduce una compra válida.') 
        time.sleep(3)
        modify_a_buy(realtime,wallet_at_use,borrado)
    if id_sell == 'a' or id_sell == 'A':
        db_manager_menu(realtime,wallet_at_use,borrado)           
    if not isinstance(id_sell, int):
        print('Solo se permiten valores numéricos.')
        time.sleep(3)
        modify_a_buy(wallet_at_use, borrado)

    else:
        opcion = input('Que deseas modificar?\n'
              '[A]Buy price\n'
              '[B]Taxes\n'
              '[C]Qty\n'
              )
        if opcion == 'A' or opcion =='a':
            new_price = input('Cual es el nuevo precio?')
            cursor.execute(f'UPDATE stock_wallet_{user_at_use} SET buy_price = {new_price} WHERE id_buy = {id_sell}')
            user_conn.commit()
            cursor.execute(f'SELECT buy_price, taxes, qty FROM stock_wallet_{user_at_use} WHERE id_buy = {id_sell}')
            data_from_table = cursor.fetchone()
            buy_price = data_from_table[0]
            taxes = data_from_table[1]
            qty = data_from_table[2]
            accountcharge = (buy_price * qty) + taxes
            cursor.execute(f'UPDATE stock_wallet_{user_at_use} SET accountcharge = {accountcharge} WHERE id_buy = {id_sell}')
            user_conn.commit()
            cursor.close()
            user_conn.close()
            #Conectamos ahora con la db de balances para comprobar si hay alguna venta referida a esa compra.

            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'SELECT id_buy FROM balances_{user_at_use}')
            num_registros = cursor.fetchone()
            

            if id_sell in num_registros:
                cursor.close()
                user_conn.close()
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')  
                cursor = user_conn.cursor()
                cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_sell}')   
                buy_charge = cursor.fetchone()[0]
                cursor.close()
                user_conn.close()
                #Sacamos el cargo en cuenta actualizado
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db') 
                cursor = user_conn.cursor()
                cursor.execute(f'SELECT accountincome FROM stock_sales_{user_at_use} WHERE id_buy = {id_sell}')
                sell_income = cursor.fetchone()[0]
                cursor.close()
                user_conn.close()
                #Sacamos el ingreso en cuenta de la venta
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
                cursor = user_conn.cursor()
                new_balance = sell_income - buy_charge
                cursor.execute(f'UPDATE balances_{user_at_use} SET balance = {new_balance} WHERE id_buy = {id_sell}')
                user_conn.commit()
                cursor.execute(f'UPDATE balances_{user_at_use} SET buy_price = {new_price} WHERE id_buy = {id_sell}')
                user_conn.commit()
                cursor.close()
                user_conn.close()
                 #Cerramos la conexion , conectamos con la db de balances de nuevo y le updateamos el balance.
                 #Cerramos conexion y hacemos commit.
            else:
                os.system(borrado
                           )
                print('Compra con sus respectivos adjuntos modificados y refrescados.')
                time.sleep(3)
                os.system(borrado)
                db_manager_menu(realtime,wallet_at_use,borrado)
      
        if opcion == 'B' or opcion == 'b':
            
            new_taxes = input('Cuales son las nuevas comisiones?')
            cursor.execute(f'UPDATE stock_wallet_{user_at_use} SET taxes = {new_taxes} WHERE id_buy = {id_sell}')
            user_conn.commit()
            cursor.execute(f'SELECT buy_price, taxes, qty FROM stock_wallet_{user_at_use} WHERE id_buy = {id_sell}')
            data_from_table = cursor.fetchone()
            buy_price = data_from_table[0]
            taxes = data_from_table[1]
            qty = data_from_table[2]
            accountcharge = (buy_price * qty) + taxes
            cursor.execute(f'UPDATE stock_wallet_{user_at_use} SET accountcharge = {accountcharge} WHERE id_buy = {id_sell}')
            user_conn.commit()
            cursor.close()
            user_conn.close()
            #Conectamos ahora con la db de balances para comprobar si hay alguna venta referida a esa compra.

            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'SELECT id_buy FROM balances_{user_at_use}')
            num_registros = cursor.fetchone()

            if id_sell in num_registros:
                cursor.close()
                user_conn.close()
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')  
                cursor = user_conn.cursor()
                cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_sell}')   
                buy_charge = cursor.fetchone()[0]
                cursor.close()
                user_conn.close()
                #Sacamos el cargo en cuenta actualizado
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db') 
                cursor = user_conn.cursor()
                cursor.execute(f'SELECT accountincome FROM stock_sales_{user_at_use} WHERE id_buy = {id_sell}')
                sell_income = cursor.fetchone()[0]
                cursor.close()
                user_conn.close()
                #Sacamos el ingreso en cuenta de la venta
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
                cursor = user_conn.cursor()
                new_balance = sell_income - buy_charge
                cursor.execute(f'UPDATE balances_{user_at_use} SET balance = {new_balance} WHERE id_buy = {id_sell}')
                user_conn.commit()
                cursor.execute(f'UPDATE balances_{user_at_use} SET taxes = {new_taxes} WHERE id_buy = {id_sell}')
                user_conn.commit()
                cursor.close()
                user_conn.close()
                 #Cerramos la conexion , conectamos con la db de balances de nuevo y le updateamos el balance.
                 #Cerramos conexion y hacemos commit.
            else:
                os.system(borrado
                           )
                print('Compra con sus respectivos adjuntos modificados y refrescados.')
                time.sleep(3)
                os.system(borrado)
                db_manager_menu(realtime,wallet_at_use,borrado)
        
        if opcion == 'C' or opcion == 'c':
            new_qty = input('Que cantidad es la correcta?')
            cursor.execute(f'UPDATE stock_wallet_{user_at_use} SET qty = {new_qty} WHERE id_buy = {id_sell}')
            user_conn.commit()
            cursor.execute(f'SELECT buy_price, taxes, qty FROM stock_wallet_{user_at_use} WHERE id_buy = {id_sell}')
            data_from_table = cursor.fetchone()
            buy_price = data_from_table[0]
            taxes = data_from_table[1]
            qty = data_from_table[2]
            accountcharge = (buy_price * qty) + taxes
            cursor.execute(f'UPDATE stock_wallet_{user_at_use} SET accountcharge = {accountcharge} WHERE id_buy = {id_sell}')
            user_conn.commit()
            cursor.close()
            user_conn.close()
            #Conectamos ahora con la db de balances para comprobar si hay alguna venta referida a esa compra.

            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'SELECT id_buy FROM balances_{user_at_use}')
            num_registros = cursor.fetchone()

            if id_sell in num_registros:
                cursor.close()
                user_conn.close()
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')  
                cursor = user_conn.cursor()
                cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_sell}')   
                buy_charge = cursor.fetchone()[0]
                cursor.close()
                user_conn.close()
                #Sacamos el cargo en cuenta actualizado
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db') 
                cursor = user_conn.cursor()
                cursor.execute(f'SELECT accountincome FROM stock_sales_{user_at_use} WHERE id_buy = {id_sell}')
                sell_income = cursor.fetchone()[0]
                cursor.close()
                user_conn.close()
                #Sacamos el ingreso en cuenta de la venta
                user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
                cursor = user_conn.cursor()
                new_balance = sell_income - buy_charge
                cursor.execute(f'UPDATE balances_{user_at_use} SET balance = {new_balance} WHERE id_buy = {id_sell}')
                user_conn.commit()
                cursor.execute(f'UPDATE balances_{user_at_use} SET qty = {new_qty} WHERE id_buy = {id_sell}')
                user_conn.commit()
                cursor.close()
                user_conn.close()
                 #Cerramos la conexion , conectamos con la db de balances de nuevo y le updateamos el balance.
                 #Cerramos conexion y hacemos commit.  
            else:
                os.system(borrado
                           )
                print('Compra con sus respectivos adjuntos modificados y refrescados.')
                time.sleep(3)
                os.system(borrado)
                db_manager_menu(realtime,wallet_at_use,borrado)     
                  


def modify_a_sell(realtime,wallet_at_use,borrado):
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
        #Hemos seleccionado el usuario, viendo lo que se repite, hare una funcion a parte para esto.
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
    sell_df = pd.read_sql(f'SELECT * FROM stock_sales_{user_at_use}',user_conn,)
    sell_df = sell_df.reset_index(drop=True)
    sell_df = sell_df.set_index('id_buy')
    print(sell_df)

    #Imprimimos por df la tabla de las compras usando Pandas como consultor.Tambien deberia de hacer una funcion para esto.
    #Still learning!
    cursor = user_conn.cursor()
    id_sell = int(input('Que venta deseas modificar?\n'
                       '[A]Para ir atras.'))
    cursor.execute(f'SELECT id_buy FROM stock_sales_{user_at_use}')
    num_registros = cursor.fetchall()

    if id_sell not in num_registros[0]:
        print('Venta no encontrada, introduce una venta válida.') 
        time.sleep(3)
        modify_a_sell(realtime,wallet_at_use,borrado)
    if id_sell == 'a' or id_sell == 'A':
        db_manager_menu(realtime,wallet_at_use,borrado)           
    if not isinstance(id_sell, int):
        print('Solo se permiten valores numéricos.')
        time.sleep(3)
        modify_a_sell(wallet_at_use, borrado)

    else:
        opcion = input('Que deseas modificar?\n'
                       '[A]Sell price\n'
                       '[B]Taxes\n'
                       '[C]Qty\n')
        if opcion == 'A' or opcion == 'a':
            new_price = input('Cual es el nuevo precio?')
            cursor.execute(f'UPDATE stock_sales_{user_at_use} SET sell_price = {new_price} WHERE id_sale = {id_sell}')
            user_conn.commit()
            cursor.execute(f'SELECT sell_price, taxes, qty, id_buy FROM stock_sales_{user_at_use} WHERE id_sale = {id_sell}')
            data_from_table = cursor.fetchone()
            sell_price = data_from_table[0]
            taxes = data_from_table[1]
            qty = data_from_table[2]
            id_buy = data_from_table[3]
            accountincome = (sell_price * qty) - taxes             
            cursor.execute(f'UPDATE stock_sales_{user_at_use} SET accountincome = {accountincome} WHERE id_sale = {id_sell}')      
            user_conn.commit()
            cursor.close()
            user_conn.close()
            #En este caso no hay que comprobar en otra db ya que es una venta que se sobreentiende que antes ha tenido que haber
            #una compra. Asi que simplemente se actualiza el balance final en la tabla balances_{user_at_use}.db
            
            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')   
            buy_charge = cursor.fetchone()[0]
            cursor.close()
            user_conn.close()
            #Sacamos el cargo en cuenta
            new_balance = accountincome - buy_charge
            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'UPDATE balances_{user_at_use} SET balance = {new_balance} WHERE id_buy = {id_buy}')
            cursor.execute(f'UPDATE balances_{user_at_use} SET sell_price = {new_price} WHERE id_buy = {id_buy}')
            user_conn.commit()
            cursor.close()
            user_conn.close()
        
        if opcion == 'B' or opcion == 'b':
            new_taxes = input('Cuales son las nuevas comisiones?')
            cursor.execute(f'UPDATE stock_sales_{user_at_use} SET taxes = {new_taxes} WHERE id_sale = {id_sell}')
            user_conn.commit()
            cursor.execute(f'SELECT sell_price, taxes, qty, id_buy FROM stock_sales_{user_at_use} WHERE id_sale = {id_sell}')
            data_from_table = cursor.fetchone()
            sell_price = data_from_table[0]
            taxes = data_from_table[1]
            qty = data_from_table[2]
            id_buy = data_from_table[3]
            accountincome = (sell_price * qty) - taxes             
            cursor.execute(f'UPDATE stock_sales_{user_at_use} SET accountincome = {accountincome} WHERE id_sale = {id_sell}')      
            user_conn.commit()
            cursor.close()
            user_conn.close()
            #En este caso no hay que comprobar en otra db ya que es una venta que se sobreentiende que antes ha tenido que haber
            #una compra. Asi que simplemente se actualiza el balance final en la tabla balances_{user_at_use}.db
            
            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
            cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')   
            buy_charge = cursor.fetchone()[0]
            cursor.close()
            user_conn.close()
            #Sacamos el cargo en cuenta
            new_balance = accountincome - buy_charge
            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'UPDATE balances_{user_at_use} SET balance = {new_balance} WHERE id_buy = {id_buy}')
            cursor.execute(f'UPDATE balances_{user_at_use} SET sell_price = {new_price} WHERE id_buy = {id_buy}')
            user_conn.commit()
            cursor.close()
            user_conn.close()
        
        if opcion == 'C' or opcion == 'c':
            new_qty = input('Cual es la nueva cantidad?')
            cursor.execute(f'UPDATE stock_sales_{user_at_use} SET qty = {new_qty} WHERE id_sale = {id_sell}')
            user_conn.commit()
            cursor.execute(f'SELECT sell_price, taxes, qty, id_buy FROM stock_sales_{user_at_use} WHERE id_sale = {id_sell}')
            data_from_table = cursor.fetchone()
            sell_price = data_from_table[0]
            taxes = data_from_table[1]
            qty = data_from_table[2]
            id_buy = data_from_table[3]
            accountincome = (sell_price * qty) - taxes             
            cursor.execute(f'UPDATE stock_sales_{user_at_use} SET accountincome = {accountincome} WHERE id_sale = {id_sell}')      
            user_conn.commit()
            cursor.close()
            user_conn.close()
            #En este caso no hay que comprobar en otra db ya que es una venta que se sobreentiende que antes ha tenido que haber
            #una compra. Asi que simplemente se actualiza el balance final en la tabla balances_{user_at_use}.db
            
            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
            cursor.execute(f'SELECT accountcharge FROM stock_wallet_{user_at_use} WHERE id_buy = {id_buy}')   
            buy_charge = cursor.fetchone()[0]
            cursor.close()
            user_conn.close()
            #Sacamos el cargo en cuenta
            new_balance = accountincome - buy_charge
            user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
            cursor = user_conn.cursor()
            cursor.execute(f'UPDATE balances_{user_at_use} SET balance = {new_balance} WHERE id_buy = {id_buy}')
            cursor.execute(f'UPDATE balances_{user_at_use} SET sell_price = {new_price} WHERE id_buy = {id_buy}')
            user_conn.commit()
            cursor.close()
            user_conn.close()    

def find_a_buy(realtime,wallet_at_use,borrado):
    
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    
    
    option = input('¿Qué filtro deseas usar para encontrar tu compra?\n'
                   '[A]Nombre valor\n'
                   '[B]Fecha de compra\n'
                   '[C]Cantidad\n'
                   '[D]Volver atrás\n'
                   )
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')  
    os.system(borrado)
    
    if option == 'a' or option == 'A':
        name_of_buy = input('Cual es el nombre del valor?\n')
        df = pd.read_sql_query(f'SELECT * from stock_wallet_{user_at_use} WHERE stock LIKE "%{name_of_buy}%" ', user_conn)
        print(df)
        print(f'\nTe muestro los resultados de la busqueda basados en el criterio = {name_of_buy}\n')
        input('\nPresiona ENTER para continuar')
        user_conn.close()
        os.system(borrado)
        db_manager_menu(realtime,wallet_at_use,borrado)
    
    if option =='b' or option == 'B':
        date_of_buy = input('Cual es la fecha?*\n'
                            '*La fecha se almacena en la base de datos de la siguiente forma:\n'
                            'AAAA-MM-DD, téngalo en cuenta a la hora de tu criterio de búsqueda' )

        df = pd.read_sql_query(f'SELECT * from stock_wallet_{user_at_use} WHERE date LIKE "%{date_of_buy}%" ', user_conn)
        print(df)
        print(f'\nTe muestro los resultados de la busqueda basados en el criterio = {date_of_buy}\n')
        input('\nPresiona ENTER para continuar')
        user_conn.close()
        os.system(borrado)
        db_manager_menu(realtime,wallet_at_use,borrado)
    
    if option == 'c' or option == 'C':
        qty_of_buy = input('Que cantidad de acciones desdeas filtrar?')
        df = pd.read_sql_query(f'SELECT * from stock_wallet_{user_at_use} WHERE qty LIKE "{qty_of_buy}" ', user_conn)
        print(df)
        print(f'\nTe muestro los resultados de la busqueda basados en el criterio = {qty_of_buy}\n')
        input('\nPresiona ENTER para continuar')
        user_conn.close()
        os.system(borrado)
        db_manager_menu(realtime,wallet_at_use,borrado)
    if option == 'q' or option == 'Q':
        db_manager_menu(realtime,wallet_at_use,borrado)
    
    else :
        print('Introduce un valor correcto.')
        find_a_buy(realtime,wallet_at_use,borrado)

def find_a_sale(realtime,wallet_at_use,borrado):

    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    
    
    option = input('¿Qué filtro deseas usar para encontrar tu compra?\n'
                   '[A]Nombre valor\n'
                   '[B]Fecha de compra\n'
                   '[C]Cantidad\n'
                   '[D]Volver atrás'
                   )
    user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')

    if option == 'a' or option == 'A':
        name_of_sale = input('Cual es el nombre del valor?\n')
        df = pd.read_sql_query(f'SELECT * from stock_sales_{user_at_use} WHERE stock LIKE "%{name_of_sale}%" ', user_conn)
        print(df)
        print(f'\nTe muestro los resultados de la busqueda basados en el criterio = {name_of_sale}\n')
        input('\nPresiona ENTER para continuar')
        user_conn.close()
        os.system(borrado)
        db_manager_menu(realtime,wallet_at_use,borrado)

    if option =='b' or option == 'B':
        date_of_sale = input('Cual es la fecha?*\n'
                            '*La fecha se almacena en la base de datos de la siguiente forma:\n'
                            'AAAA-MM-DD, téngalo en cuenta a la hora de tu criterio de búsqueda' )

        df = pd.read_sql_query(f'SELECT * from stock_sales_{user_at_use} WHERE date LIKE "%{date_of_sale}%" ', user_conn)
        print(df)
        print(f'\nTe muestro los resultados de la busqueda basados en el criterio = {date_of_sale}\n')
        input('\nPresiona ENTER para continuar')
        user_conn.close()
        os.system(borrado)
        db_manager_menu(realtime,wallet_at_use,borrado)
    
    if option == 'c' or option == 'C':
        qty_of_sale = input('Que cantidad de acciones desdeas filtrar?')
        df = pd.read_sql_query(f'SELECT * from stock_sales_{user_at_use} WHERE qty LIKE "{qty_of_sale}" ', user_conn)
        print(df)
        print(f'\nTe muestro los resultados de la busqueda basados en el criterio = {qty_of_sale}\n')
        input('\nPresiona ENTER para continuar')
        user_conn.close()
        os.system(borrado)
        db_manager_menu(realtime,wallet_at_use,borrado)
    if option == 'q' or option == 'Q':
        db_manager_menu(realtime,wallet_at_use,borrado)
    
    else :
        print('Introduce un valor correcto.')
        find_a_sale(realtime,wallet_at_use,borrado)


def show_wallet(realtime,wallet_at_use,borrado):
    
    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()
    
    option = input('[A]Muestra todas las compras\n'
                   '[B]Muestra tus compras ,junto a sus ventas.\n'
                   '[C]Muestra las compras pendientes de venta.\n'
                   '[D]Volver atras.\n')
    
    if option == 'A' or option == 'a':
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')  
        wallet_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn)
        print(wallet_df)
        input('\nPulsa ENTER para continuar.\n')
        os.system(borrado)
        time.sleep(2)
        user_conn.close()
        show_wallet(realtime,wallet_at_use,borrado)

    if option == 'B' or option == 'b':
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
        wallet_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn)
        user_conn.close()
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
        wallet_df_sales = pd.read_sql(f'SELECT * FROM stock_sales_{user_at_use}',user_conn)
        user_conn.close()
        wallet_df_merged = pd.merge(wallet_df, wallet_df_sales, on='id_buy',how='inner',suffixes=(' Compra',' Venta'))
        wallet_df_merged = wallet_df_merged.rename(columns=str.upper)
        print(wallet_df_merged)
        input('\nPulsa ENTER para continuar.\n')
        os.system(borrado)
        time.sleep(2)
        show_wallet(realtime,wallet_at_use,borrado)

    if option == 'C' or option == 'c':
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
        wallet_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn)
        user_conn.close()
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
        wallet_df_sales = pd.read_sql(f'SELECT * FROM stock_sales_{user_at_use}',user_conn)
        user_conn.close()
        wallet_df_merged_notin = wallet_df[~wallet_df['id_buy'].isin(wallet_df_sales['id_buy'])]
        wallet_df_merged_notin = wallet_df_merged_notin.rename(columns=str.upper)
        print(wallet_df_merged_notin)
        input('\nPulsa ENTER para continuar.\n')
        os.system(borrado)
        time.sleep(2)
        show_wallet(realtime,wallet_at_use,borrado)       
    if option == 'D' or option == 'd':
        os.system(borrado)
        time.sleep(2)
        db_manager_menu(realtime,wallet_at_use,borrado)

def show_sales(realtime,wallet_at_use,borrado):

    user_conn = sqlite3.connect('./db/user.db')
    cursor = user_conn.cursor()
    cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
    user_at_use = cursor.fetchone()
    user_at_use = user_at_use[1]
    cursor.close()
    user_conn.close()

    option = input('[A]Muestra todas las ventas efectuadas.\n'
                   '[B]Muestra todas las ventas junto a sus compras y el balance final.\n'
                   '[C]Volver atras.\n')
    
    if option == 'A' or option == 'a':
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
        wallet_df_sales = pd.read_sql(f'SELECT * FROM stock_sales_{user_at_use}',user_conn)
        wallet_df_sales = wallet_df_sales.rename(columns=str.upper)
        user_conn.close()
        print(wallet_df_sales)
        input('\nPulsa ENTER para continuar.\n')
        os.system(borrado)
        time.sleep(2)
        show_sales(realtime,wallet_at_use,borrado)   
    
    if option == 'B' or option == 'b':
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/balances_{user_at_use}.db')
        wallet_df_balances = pd.read_sql(f'SELECT * FROM balances_{user_at_use}',user_conn)
        user_conn.close()
        wallet_df_balances = wallet_df_balances.rename(columns=str.upper)
        print(wallet_df_balances)
        input('\nPulsa ENTER para continuar.\n')
        os.system(borrado)
        time.sleep(2)
        show_sales(realtime,wallet_at_use,borrado) 
    
    if option == 'c' or option == 'C':
        os.system(borrado)
        time.sleep(2)
        db_manager_menu(realtime,wallet_at_use,borrado)

def db_manager_menu(realtime,wallet_at_use,borrado):
    option = input('¿Qué desea hacer con su Wallet?\n'
                   '[A]Añadir compra a la cartera.\n'
                   '[B]Añadir venta de la cartera.\n'
                   '[C]Eliminar compra de la cartera.\n'
                   '[D]Eliminar venta de la cartera.\n'
                   '[E]Modificar compra de la cartera.\n'
                   '[F]Modificar venta de la cartera.\n'
                   '[G]Buscar compra en la cartera.\n'
                   '[H]Buscar venta en la cartera.\n'
                   '[I]Ver cartera actual.\n'
                   '[J]Ver ventas efectuadas.\n'
                   '[K]Volver atrás.\n')
    
    if option == 'A' or option == 'a':
        os.system(borrado)
        add_to_wallet(realtime,wallet_at_use,borrado)
    
    if option == 'B' or option == 'b':
        os.system(borrado)
        add_a_sell(realtime,wallet_at_use,borrado)

    if option == 'C' or option == 'c':
        os.system(borrado)
        delete_a_buy(realtime,wallet_at_use,borrado)

    if option == 'D' or option == 'd':
        os.system(borrado)
        delete_a_sell(realtime,wallet_at_use,borrado)

    if option == 'E' or option == 'e':
        os.system(borrado)
        modify_a_buy(realtime,wallet_at_use,borrado)

    if option == 'F' or option == 'f':
        os.system(borrado)
        modify_a_sell(realtime,wallet_at_use,borrado)
        
    if option == 'G' or option == 'g':
        os.system(borrado)
        find_a_buy(realtime,wallet_at_use,borrado)
        
    if option == 'H' or option == 'h':
        os.system(borrado)
        find_a_sale(realtime,wallet_at_use,borrado)
       
    if option == 'I' or option == 'i':
        os.system(borrado)
        show_wallet(realtime,wallet_at_use,borrado)
     
    if option == 'J' or option =='j':
       os.system(borrado)
       show_sales(realtime,wallet_at_use,borrado)
       
    if option == 'K' or option == 'k':
       os.system(borrado)
       main_menu(realtime,wallet_at_use,borrado)