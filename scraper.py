from wallettraker_srcs import requests, BeautifulSoup, os, URL, pd, time, sqlite3, keyboard, color_column, Fore, Style
import main

def urlcontent(url):
    result = requests.get(url)
    return result


def scrapurl(result):
    realtime = []
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_= "ellipsis-short")
    price_scrap = url_content.find_all(class_="tv-price")
    time_scrap = url_content.find_all(class_="tv-time")
    close_scrap = url_content.find_all(class_="tv-close")
    var_scrap = url_content.find_all(class_="tv-change-percent")
    more_or_less_scrap = url_content.find_all(class_="tv-change-abs")
    
    acciones = []
    precio_acciones = []
    tiempo_acciones = []
    var_acciones = []
    close_acciones = []
    more_or_less_acciones = []

    for acc in acc_scrap:
        acc = acc.text.replace("\t","").replace("\r","").replace("\n","")
        acciones.append(acc)
    for price in price_scrap:
        if "\nPrecio\n" not in price.text:
            price = price.text.replace("\n","").replace(",",".")
            precio_acciones.append(float(price))
    for time in time_scrap:
        if "\nÚLTIMA ACTUALIZACIÓN\n" not in time.text:
            time = time.text.replace("\n","")
            tiempo_acciones.append(time)
    for var in var_scrap:
        if "\n%\n" not in var.text:
            var = var.text.replace("\n","")
            var_acciones.append(var) 
    for close in close_scrap:
        if "\nPRECIO DE CIERRE\n" not in close.text:
            close = close.text.replace("\n","").replace("\t","").replace("\r","")
            close_acciones.append(close)
    for more_or_less in more_or_less_scrap:
        if "\n+/-" not in more_or_less.text:
            more_or_less = more_or_less.text.replace("\n","").replace(',','.')
            more_or_less_acciones.append(more_or_less)
    for Stock, Price, Time, Var, Close, VarinPercent in zip(acciones, precio_acciones, tiempo_acciones, var_acciones, 
                                                            close_acciones, more_or_less_acciones):
        value = {"Stock":Stock, "Price":Price, "Time":Time, "%":Var, "Close":Close, "+/-":VarinPercent}
        realtime.append(value) 
    return realtime


def show_tiempo_real(realtime,borrado):
    
    while True:
        realtime = []
        os.system(borrado)
        result = urlcontent(URL)          
        realtime = scrapurl(result)
        df = pd.DataFrame(realtime)
        columns_to_modify = ['Price','Close','+/-']
        df[columns_to_modify] = df[columns_to_modify].apply(lambda x: x.astype(str) + '€')
        print(df)
        time.sleep(5)


def show_tiempo_real_with_wallet(realtime,wallet_at_use,borrado,colors):
    
    exit_key = 'q'

    while not keyboard.is_pressed(exit_key):
        
        
        realtime = []
        os.system(borrado)
        result = urlcontent(URL)          
        realtime = scrapurl(result)
        df = pd.DataFrame(realtime)


        user_conn = sqlite3.connect('./db/user.db')
        cursor = user_conn.cursor()
        cursor.execute(f'SELECT * FROM user WHERE id={wallet_at_use}')
        user_at_use = cursor.fetchone()
        user_at_use = user_at_use[1]
        cursor.close()
        user_conn.close()

        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_wallet_{user_at_use}.db')
        wallet_df = pd.read_sql(f'SELECT * FROM stock_wallet_{user_at_use}',user_conn)
        user_conn.close()
        user_conn = sqlite3.connect(f'./db/user/{user_at_use}/stock_sales_{user_at_use}.db')
        wallet_df_sales = pd.read_sql(f'SELECT * FROM stock_sales_{user_at_use}',user_conn)
        user_conn.close()
        wallet_df_merged_notin = wallet_df[~wallet_df['id_buy'].isin(wallet_df_sales['id_buy'])]
        wallet_df_merged_notin = wallet_df_merged_notin.rename(columns=str.capitalize)
        
        wallet_df_merged_notin_result = pd.merge(df, wallet_df_merged_notin, on='Stock')
       

        wallet_df_merged_notin_result['Balance'] = (
            wallet_df_merged_notin_result['Price'] * wallet_df_merged_notin_result['Qty']
            ) - wallet_df_merged_notin_result['Accountcharge']
        


        columns_to_modify = ['Price','Close','+/-']
        columns_to_modify2 = ['Price','Close','+/-','Buy_price','Accountcharge','Balance']
      
        wallet_df_merged_notin_result = wallet_df_merged_notin_result.drop(['Index','Id_buy'],axis=1)
        wallet_df_merged_notin_result['Accountcharge'] = wallet_df_merged_notin_result['Accountcharge'].apply(lambda x: round(x,2))
        wallet_df_merged_notin_result['Balance'] = wallet_df_merged_notin_result['Balance'].apply(lambda x: round(x,2))
        
        colors_for_df = ['+/-']
        colors_for_wallet_df = ['+/-','Balance']
        
        df['+/-'] = df["+/-"].astype(float)
        wallet_df_merged_notin_result['+/-'] = wallet_df_merged_notin_result["+/-"].astype(float)

        '''for col in colors_for_df:
            df[col] = df[col].apply(colors)
            
        for col in colors_for_wallet_df:   
            wallet_df_merged_notin_result[col] = wallet_df_merged_notin_result[col].apply(colors)
        
        df[columns_to_modify] = df[columns_to_modify].apply(lambda x: x.astype(str) + '€')
        wallet_df_merged_notin_result[columns_to_modify2] = wallet_df_merged_notin_result[columns_to_modify2].apply(lambda x: x.astype(str) + '€' )
        
        pd.set_option('display.width', None)
        pd.set_option('display.expand_frame_repr', False)
        '''
        print(Fore.CYAN + '\nIBEX 35\n' + '-' * 7)
        print(Style.RESET_ALL)
        print(df)
        
        print(Fore.GREEN + '\nVALORES EN CARTERA\n' + '-' * 18)
        print(Style.RESET_ALL)
        print(wallet_df_merged_notin_result)
        
        
        
        time.sleep(10)

    main.main_menu(realtime,wallet_at_use,borrado)    