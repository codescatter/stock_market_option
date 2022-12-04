import pyotp
from NorenRestApiPy.NorenApi import NorenApi
import time
import numpy as np
import concurrent.futures

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                          websocket='wss://api.shoonya.com/NorenWSTP/',
                          eodhost='https://shoonya.finvasia.com/chartApi/getdata/')


import logging

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

# start of our program
api = ShoonyaApiPy()

# credentials
user = 'FA62511'
token = "42XL2J5434C46V7OVG3S2U52ASZTV3DE"
pwd = 'Awinash@12'
vc = "FA62511_U"
app_key = 'eacdb6b5dca7ad2f01b173c0da240338'
imei = 'abc1234'

# make the api call
ret = api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei)
print(ret)


def buy_order(symbol):
    ret = api.place_order(buy_or_sell='B', product_type='I',
                          exchange='NFO', tradingsymbol=symbol,
                          quantity=25, discloseqty=0, price_type='MKT', price=0, trigger_price=0,
                          retention='DAY', remarks='my_order_001')

    return ret

def sell_order(symbol, quentity):
    ret = api.place_order(buy_or_sell='S', product_type='I', exchange='NFO', tradingsymbol=symbol,
                    quantity=quentity, discloseqty=0, price_type='MKT', price=0,
                    trigger_price=0, retention='DAY', remarks='my_order_001')

    return ret

def exit_order(orderno):
    ret = api.exit_order(orderno, product_type=None)

    return ret


def gettig_current_price(exchange, token):
    one = api.get_quotes(exchange=exchange, token=token)
    current_price = one["lp"]

    return float(current_price)


flag=True
count = 0
di_desi_price = 43300


while flag:
    pos = api.get_positions()
    p_l = 0
    for own_pos in pos:
        p_l+=float(own_pos["rpnl"])
    if p_l>-1000 and p_l<2000:
        if count<20:
            time.sleep(1)
            current_price = gettig_current_price(exchange = "NFO", token = "62808")
            if current_price>=di_desi_price:
                symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                ret = buy_order(symbol)

                own_flag = True
                sell_target=[]
                quentity_main = 25
                while own_flag:
                    time.sleep(1)
                    current_price1 = gettig_current_price(exchange="NFO", token="62808")
                    if current_price1==di_desi_price+100:
                        symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                        ret_sell = sell_order(symbol, quentity=quentity_main)
                        di_desi_price = di_desi_price + 100
                        count=0
                        own_flag = False
                    # elif current_price1>=di_desi_price+30 and current_price1<=di_desi_price+35 and "30" not in sell_target:
                    #     symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                    #     ret_sell = sell_order(symbol, quentity=25)
                    #     sell_target.append("30")
                    #     quentity_main=quentity_main-25
                    # elif current_price1>=di_desi_price+80 and current_price1<=di_desi_price+85 and "80" not in sell_target:
                    #     symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                    #     ret_sell = sell_order(symbol, quentity=25)
                    #     sell_target.append("80")
                    #     quentity_main=quentity_main-25
                    elif current_price1<=di_desi_price:
                        symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                        ret_sell = sell_order(symbol, quentity=quentity_main)
                        count+=1
                        own_flag = False
                    else:
                        pass

            elif current_price<=di_desi_price:
                symbol = f"BANKNIFTY08DEC22P{di_desi_price + 100}"
                ret = buy_order(symbol)

                sell_target = []
                quentity_main = 25
                own_flag = True
                while own_flag:
                    time.sleep(1)
                    current_price2 = gettig_current_price(exchange="NFO", token="62808")
                    if current_price2 == di_desi_price - 100:
                        symbol = f"BANKNIFTY08DEC22P{di_desi_price + 100}"
                        ret_sell = sell_order(symbol, quentity=quentity_main)
                        di_desi_price = di_desi_price - 100
                        count=0
                        own_flag = False
                    # elif current_price2<=di_desi_price-30 and current_price2>=di_desi_price-35 and "30" not in sell_target:
                    #     symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                    #     ret_sell = sell_order(symbol, quentity=25)
                    #     sell_target.append("30")
                    #     quentity_main=quentity_main-25
                    # elif current_price2<=di_desi_price-80 and current_price2>=di_desi_price-85 and "80" not in sell_target:
                    #     symbol = f"BANKNIFTY08DEC22C{di_desi_price - 100}"
                    #     ret_sell = sell_order(symbol, quentity=25)
                    #     sell_target.append("80")
                    #     quentity_main=quentity_main-25
                    elif current_price2 >= di_desi_price:
                        symbol = f"BANKNIFTY08DEC22P{di_desi_price + 100}"
                        ret_sell = sell_order(symbol, quentity=quentity_main)
                        count += 1
                        own_flag = False
                    else:
                        pass
            else:
                pass
        else:
            time.sleep(1)
            current_price = gettig_current_price(exchange="NFO", token="62808")
            if current_price==di_desi_price+100:
                di_desi_price= current_price
            elif current_price==di_desi_price-100:
                di_desi_price = current_price
            else:
                pass
    else:
        time.sleep(1)
        current_price = gettig_current_price(exchange="NFO", token="62808")
        if current_price == di_desi_price + 100:
            di_desi_price = current_price
        elif current_price == di_desi_price - 100:
            di_desi_price = current_price
        else:
            pass


