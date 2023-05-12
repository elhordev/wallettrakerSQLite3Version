from wallettraker_srcs import HEADER ,os ,time ,URL ,wallet_at_use
import db_manager
import scraper


def borrado_dep_so():
    borrado = None
    if os.name == "posix":
        borrado = "clear"
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        borrado = "cls"
    return borrado



def user_menu(borrado):
    print ("\n" + HEADER + "\n" + "-" *len(HEADER) + "\n")
    time.sleep(5)

    wallet_at_use = db_manager.choose_user()
    return wallet_at_use

   

def main():
    borrado = borrado_dep_so()
    result = scraper.urlcontent(URL)
    realtime = scraper.scrapurl(result)
    db_manager.create_db()
    wallet_at_use = user_menu(borrado)
    db_manager.add_to_wallet(realtime,wallet_at_use,borrado)
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