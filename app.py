﻿from flask import Flask, render_template_string, request, redirect, url_for
import random

app = Flask(__name__)

class SophisticatedTradingBroker:
    def __init__(self, name, starting_balance):
        self.name = name
        self.balance = starting_balance
        self.portfolio = {}

    def buy_stock(self, stock_symbol, price, shares):
        cost = price * shares
        if cost > self.balance:
            return f"Insufficient funds to buy {shares} shares of {stock_symbol}."

        self.balance -= cost
        if stock_symbol in self.portfolio:
            current_data = self.portfolio[stock_symbol]
            total_shares = current_data['shares'] + shares
            total_cost = (current_data['avg_price'] * current_data['shares']) + cost
            self.portfolio[stock_symbol] = {
                'shares': total_shares,
                'avg_price': total_cost / total_shares
            }
        else:
            self.portfolio[stock_symbol] = {
                'shares': shares,
                'avg_price': price
            }

        return f"Bought {shares} shares of {stock_symbol} @ ${price:.2f} each."

    def sell_stock(self, stock_symbol, price, shares):
        if stock_symbol not in self.portfolio or self.portfolio[stock_symbol]['shares'] < shares:
            return f"Not enough shares of {stock_symbol} to sell."

        proceeds = price * shares
        self.balance += proceeds
        self.portfolio[stock_symbol]['shares'] -= shares

        if self.portfolio[stock_symbol]['shares'] == 0:
            del self.portfolio[stock_symbol]

        return f"Sold {shares} shares of {stock_symbol} @ ${price:.2f} each."

    def get_current_price(self, stock_symbol):
        return round(random.uniform(50, 150), 2)

broker = SophisticatedTradingBroker("AlphaTrade", 10000)

@app.route('/')
def home():
    return render_template_string('''
        <h1>{{ broker.name }} - Balance: ${{ broker.balance }}</h1>
        <h2>Portfolio:</h2>
        <ul>
            {% for stock, data in broker.portfolio.items() %}
                <li>{{ stock }}: {{ data['shares'] }} shares @ ${{ data['avg_price'] }}</li>
            {% endfor %}
        </ul>
        <h2>Trade:</h2>
        <form method="post" action="/trade">
            Stock Symbol: <input type="text" name="symbol" required><br>
            Action: <select name="action">
                <option value="buy">Buy</option>
                <option value="sell">Sell</option>
            </select><br>
            Shares: <input type="number" name="shares" min="1" required><br>
            <input type="submit" value="Submit">
        </form>
        {% if message %}<p>{{ message }}</p>{% endif %}
    ''', broker=broker, message=request.args.get('message'))

@app.route('/trade', methods=['POST'])
def trade():
    symbol = request.form['symbol'].upper()
    action = request.form['action']
    shares = int(request.form['shares'])
    price = broker.get_current_price(symbol)

    if action == 'buy':
        message = broker.buy_stock(symbol, price, shares)
    elif action == 'sell':
        message = broker.sell_stock(symbol, price, shares)
    else:
        message = "Invalid action."

    return redirect(url_for('home', message=message))

if __name__ == '__main__':
    app.run(debug=True)

