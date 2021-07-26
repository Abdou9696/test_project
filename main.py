from flask import Flask, redirect, url_for, request, render_template

import requests
import json

# Initialize the Key and the endpoint
API_ENDPOINT = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?region=US&lang=en"
API_KEY = "ba1d2f78e2msh289a19bec03e479p161cafjsn1315cd23cfde"

def get_data(symbol):
    """
    Function to get the ticker data from Yahoo finance API

    :param symbol: the ticker symbol (string)
    :return: dict which contains data about the ticker
    """
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
    """
    Function to get the regular Market Previous Close of the ticker

    :param data: dict which contains data about the ticker
    :return: the regular Market Previous Close (float)
    """
    return data["summaryDetail"]["regularMarketPreviousClose"]["raw"]


app = Flask(__name__)





@app.route('/',methods = ['POST', 'GET'])
def input():
    error = None
    if request.method == 'POST':
        #get the ticker symbolr from the input and use it to get data
        symbol = request.form['symbol']
        data=get_data(symbol)
        #get the position from the input which will be used in calculation
        quantity = int(request.form['qte'])

        # if ticker symbol didn't exist, an error message will display
        if data =={}:
            error = 'Invalid ticker'
            render_template('index.html', error=error)

        else:
            # if quantity is < 0, an error message will display (but it's impossible to reach this case because
            # conditions for the insert number were added in the html page (it should be a number and > 0,
            # or the submission will not be done. By dafault the position is 1
            if quantity < 0:
                error = 'Quantity must be > 0'
                render_template('index.html', error=error)

            else:
                price = get_price(data)
                rslt = quantity * price

                #redirection for the page which will show the result
                return redirect(url_for('rslt', name=symbol.upper(), price=price, pos =quantity, notional=rslt))

    return render_template('index.html',error =error )

#The redirected page to show the result
@app.route('/<name>/<price>/<pos>/<notional>')
def rslt(name,price,pos,notional):
    return render_template('rslt.html',name=name, price=(price) ,pos =pos, notional=notional)


if __name__ == '__main__':
   app.run(debug = True)
