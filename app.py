from flask import (Response, Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)

import pyotp
from NorenRestApiPy.NorenApi import NorenApi
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'

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


def login_user(user, token, password, vender_code, app_key, imei):

    # make the api call
    ret = api.login(userid=user, password=password, twoFA=pyotp.TOTP(token).now(), vendor_code=vender_code, api_secret=app_key,
                    imei=imei)

    return ret, api


def buy_order(symbol, quentity):
    ret = api.place_order(buy_or_sell='B', product_type='I',
                          exchange='NFO', tradingsymbol=symbol,
                          quantity=quentity, discloseqty=0, price_type='MKT', price=0, trigger_price=0,
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

def getting_token_number(api, exchange, symbol):
    ret = api.searchscrip(exchange=exchange, searchtext=symbol)
    token_id = ret["values"][0].get("token")

    return token_id


def main_process(api, flag, symbol, quentity, target, p_l_profit, p_l_loss, target1, target2, target3, count_repeat, starting_point):
    count = 0
    di_desi_price = starting_point

    while flag:
        flash("process can be start")
        pos = api.get_positions()
        p_l = 0
        for own_pos in pos:
            p_l += float(own_pos["rpnl"])
        if p_l >= p_l_loss and p_l <= p_l_profit:
            if count < count_repeat:
                time.sleep(1)
                current_price = gettig_current_price(exchange="NFO", token="62808")
                if current_price >= di_desi_price and current_price<=di_desi_price+1:
                    symbol1 = f"{symbol}C{di_desi_price - 100}"
                    ret = buy_order(symbol1, quentity=quentity)

                    own_flag = True
                    sell_target = []
                    quentity_main = quentity
                    while own_flag:
                        time.sleep(1)
                        current_price1 = gettig_current_price(exchange="NFO", token="62808")
                        if current_price1 >= di_desi_price + target:
                            symbol1 = f"{symbol}C{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            di_desi_price = di_desi_price + target
                            count = 0
                            own_flag = False
                        elif target1!=0 and current_price1>=di_desi_price+target1 and current_price1<=di_desi_price+target1+15 and str(target1) not in sell_target:
                            symbol1 = f"{symbol}C{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target1))
                            quentity_main=quentity_main-25
                        elif target2!=0 and current_price1>=di_desi_price+target2 and current_price1<=di_desi_price+target2+15 and str(target2) not in sell_target:
                            symbol1 = f"{symbol}C{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target2))
                            quentity_main=quentity_main-25
                        elif target3!=0 and current_price1>=di_desi_price+target3 and current_price1<=di_desi_price+target3+15 and str(target3) not in sell_target:
                            symbol1 = f"{symbol}C{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target3))
                            quentity_main=quentity_main-25
                        elif current_price1 <= di_desi_price:
                            symbol1 = f"{symbol}C{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            count += 1
                            own_flag = False
                        else:
                            pass

                elif current_price <= di_desi_price and current_price>=di_desi_price-1:
                    symbol1 = f"{symbol}P{di_desi_price + 100}"
                    ret = buy_order(symbol1, quentity=quentity)

                    sell_target = []
                    quentity_main = quentity
                    own_flag = True
                    while own_flag:
                        time.sleep(1)
                        current_price2 = gettig_current_price(exchange="NFO", token="62808")
                        if current_price2 <= di_desi_price - target:
                            symbol1 = f"{symbol}P{di_desi_price + 100}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            di_desi_price = di_desi_price - target
                            count = 0
                            own_flag = False
                        elif target1!=0 and current_price2<=di_desi_price-target1 and current_price2>=di_desi_price-target1-15 and str(target1) not in sell_target:
                            symbol1 = f"{symbol}P{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target1))
                            quentity_main=quentity_main-25
                        elif target2!=0 and current_price2<=di_desi_price-target2 and current_price2>=di_desi_price-target2-15 and str(target2) not in sell_target:
                            symbol1 = f"{symbol}P{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target2))
                            quentity_main=quentity_main-25
                        elif target3!=0 and current_price2<=di_desi_price-target3 and current_price2>=di_desi_price-target3-15 and str(target3) not in sell_target:
                            symbol1 = f"{symbol}P{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target3))
                            quentity_main=quentity_main-25
                        elif current_price2 >= di_desi_price:
                            symbol1 = f"{symbol}P{di_desi_price + 100}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            count += 1
                            own_flag = False
                        else:
                            pass
                else:
                    pass
            else:
                time.sleep(1)
                current_price = gettig_current_price(exchange="NFO", token="62808")
                if current_price >= di_desi_price + 100:
                    di_desi_price = current_price
                elif current_price <= di_desi_price - 100:
                    di_desi_price = current_price
                else:
                    pass
        else:
            time.sleep(1)
            current_price = gettig_current_price(exchange="NFO", token="62808")
            if current_price >= di_desi_price + 100:
                di_desi_price = current_price
            elif current_price <= di_desi_price - 100:
                di_desi_price = current_price
            else:
                pass


    return "process can be complate"


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/get_token_number", methods=["GET","POST"])
def get_token_number():
    """
    That route can show landing page while user can login
    """
    try:
        if request.method == "POST":
            exchange = request.form["exchange"]
            symbol = request.form["symbol"]

            user = session.get("user", "")
            if user=="":
                flash("please add any shoonya account")
                return render_template("token.html")
            else:
                ret, api = login_user(user=session.get("user", ""), password=session.get("password", ""),
                                 vender_code=session.get("vender_code", ""),
                                 app_key=session.get("app_key", ""), imei=session.get("imei", ""),
                                 token=session.get("token", ""))

            token_number = getting_token_number(api=api, exchange=exchange, symbol=symbol)

            return render_template("token.html", token=token_number)
        else:
            return render_template("token.html")

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('filter_data', _external=True, _scheme="http"))

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/home", methods=["GET","POST"])
def home():
    """
    That route can show landing page while user can login
    """
    try:
        if request.method == "POST":
            user = request.form["user"]
            password = request.form["password"]
            vender_code = request.form["vender_code"]
            app_key = request.form["app_key"]
            imei = request.form["imei"]
            token = request.form["token"]
            symbol = request.form["symbol"]
            quentity = request.form["quentity"]
            target = request.form["target"]
            p_l_profit = request.form["p_l_profit"]
            p_l_loss = request.form["p_l_loss"]
            target1 = request.form["target1"]
            target2 = request.form["target2"]
            target3 = request.form["target3"]
            count_repeat = request.form["count_repeat"]
            starting_point = request.form["starting_point"]

            session["user"] = user
            session["password"] = password
            session["vender_code"] = vender_code
            session["app_key"] = app_key
            session["imei"] = imei
            session["token"] = token
            quentity = int(quentity)
            target = int(target)
            p_l_profit = int(p_l_profit)
            p_l_loss = int(p_l_loss)
            target1 = int(target1)
            target2 = int(target2)
            target3 = int(target3)
            count_repeat = int(count_repeat)
            starting_point = int(starting_point)

            ret, api = login_user(user=session.get("user", ""), password=session.get("password", ""), vender_code=session.get("vender_code", ""),
                       app_key=session.get("app_key", ""), imei=session.get("imei", ""), token=session.get("token", ""))

            flash("login successful")
            main_process(api=api, flag=True, symbol=symbol, quentity=quentity, target=target,
                         p_l_profit=p_l_profit, p_l_loss=p_l_loss, target1=target1,
                         target2=target2, target3=target3, count_repeat=count_repeat, starting_point=starting_point)

            return render_template("help_form.html")
        else:
            return render_template("help_form.html")

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('filter_data', _external=True, _scheme="http"))


if __name__ == "__main__":
    # db.create_all()
    app.run(
        host="127.0.0.1",
        port=8080,
        debug=True)

