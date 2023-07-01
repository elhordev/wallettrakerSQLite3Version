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
        scraper.show_tiempo_real(realtime,borrado_dep_so)
    
    if option == 'C' or option == 'c':
        scraper.show_tiempo_real_with_wallet(realtime,wallet_at_use,borrado_dep_so)
    
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

