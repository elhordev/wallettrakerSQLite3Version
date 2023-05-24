from wallettraker_srcs import HEADER ,os ,time ,URL 
import db_manager
import scraper
wallet_at_use = None

def borrado_dep_so():
    borrado = None
    if os.name == "posix":
        borrado = "clear"
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        borrado = "cls"
    return borrado



def user_menu(borrado):
    print ("\n" + HEADER + "\n" + "-" *len(HEADER) + "\n")
    time.sleep(2)

    wallet_at_use = db_manager.choose_user()
    return wallet_at_use

def main_menu(realtime,wallet_at_use,borrado_dep_so):
    option = input('¿Qué deseas hacer?:\n'
                   '[A]Gestionar tu cartera.\n'
                   '[B]Ver tiempo real.\n'
                   '[C]Ver tiempo real con tu cartera.\n'
                   '[D]Cambiar de usuario.\n'
                   '[F]Salir.\n') 
    if option == 'A' or option == 'a':
        db_manager.db_manager_menu(realtime,wallet_at_use,borrado_dep_so)
    
    if option == 'B' or option == 'b':
        scraper.show_tiempo_real()
    
    if option == 'C' or option == 'c':
        print('Aqui llamaremos a la nueva funcion de tiempo real con cartera')
    
    if option == 'D' or option == 'd':
        user_menu()

    if option == 'F' or option == 'f':
        exit()

def main():
    borrado = borrado_dep_so()
    result = scraper.urlcontent(URL)
    realtime = scraper.scrapurl(result)
    db_manager.create_db()
    wallet_at_use = user_menu(borrado)
    main_menu(realtime,wallet_at_use,borrado)
    #db_manager.add_to_wallet(realtime,wallet_at_use,borrado)
    #scraper.show_tiempo_real(realtime,borrado)
    
    user_menu(borrado)
    





if __name__ == '__main__':
    main()

"""type_wallet = input("Como deseas trabajar?\n"
                                "[A]Importar Wallet.\n"
                                "[B]Wallet Temporal.\n"
                                "[Q]Para Salir\n\n")
    os.system(borrado)
    while type_wallet != "Q" and type_wallet != "q":
            
        if type_wallet == "A" or type_wallet == "a":
                wallet_total = upload_wallet()
                return wallet_total
        if type_wallet == "b" or type_wallet == "B":
                wallet_total = []
                return wallet_total
            
    print("Hasta la proxima!")
    exit()   

"""