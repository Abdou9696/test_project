from flask import Flask, redirect, url_for, request, render_template, flash

import requests
import json

from jinja2 import Markup

API_ENDPOINT = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?region=US&lang=en"
API_KEY = "ba1d2f78e2msh289a19bec03e479p161cafjsn1315cd23cfde"






def get_data(symbol):
    response = requests.get(
        API_ENDPOINT,
        headers={'X-RapidAPI-Key': API_KEY},
        params={'symbol': symbol}
    )
    if response:
        return response.json()
    else:
        return ("Error retrieving API data for " + symbol)



def get_price(data):
    return data["summaryDetail"]["regularMarketPreviousClose"]["raw"]


app = Flask(__name__)


@app.route('/<name>/<price>/<pos>/<notional>')
def home(name,price,pos,notional):

    return render_template('rslt.html',name=name, price=price ,pos =pos, notional=notional)


@app.route('/',methods = ['POST', 'GET'])
def l():
    error = None
    if request.method == 'POST':

        symbol = (request.form['symbol'])
        data=get_data(symbol)
        if data =={}:
            error = 'Invalid ticker'
            render_template('index.html', error=error)
        else:
            quantity = int(request.form['qte'])
            if quantity < 0:
                error = 'Quantity must be > 0'
                render_template('index.html', error=error)
            else:
                price = get_price(data)
                rslt = quantity * price
                return redirect(url_for('home', name=symbol, price=price, pos =quantity, notional=rslt))

    return render_template('index.html',error =error )



if __name__ == '__main__':
   app.run(debug = True)
