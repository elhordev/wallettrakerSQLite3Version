from wallettraker_srcs import requests, BeautifulSoup, os, URL, pd, time
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
            more_or_less = more_or_less.text.replace("\n","")
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


