import os 
import db_manager
import time
HEADER = "Wellcome to wallettraker v1.0 SQLite3 Version by elhorDev"

def borrado_dep_so():
    borrado = None
    if os.name == "posix":
        borrado = "clear"
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        borrado = "cls"
    return borrado



def wellcome_menu(borrado):
    print ("\n" + HEADER + "\n" + "-" *len(HEADER) + "\n")
    time.sleep(5)
    db_manager.choose_user()


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

def main():
    borrado = borrado_dep_so()
    wellcome_menu(borrado)
    





if __name__ == '__main__':
    main()