from flask import Flask, request, jsonify, url_for
import requests 
from datetime import datetime, timedelta

app = Flask(__name__)

today = datetime.now().date()
format_date = today.strftime("%Y-%m-%d")
yesterday = today - timedelta(days=1)

@app.route('/')
def index():
    menu = f'''
        To exchange PLN to other currency go <a href="{ url_for('pln_cantor') }">here</a><br>
        To exchange other currency, go <a href="{ url_for('cantor') }">here</a><br>
'''
    return f"<h1>Hello!</h1><br>{menu}"

@app.route('/plncantor', methods=['GET', 'POST'])
def pln_cantor():

    if request.method == 'GET':
        body = f'''
            <form id="exchange_form" action="{ url_for('get_data') }" method="POST">
                <label for="amount">Enter your PLN amount:</label>
                <input type="number" id="amount" name="amount" required min="0" step="any"><br>
                <label for="currency">Choose a currency:</label>
                <select id="currency" name="currency">
                    <option value="eur">Euro</option>
                    <option value="usd">USD</option>
                    <option value="chf">CHF</option>
                    <option value="gbp">GBP</option>
                </select>
                <input type="submit" value="Submit">
            </form>
        '''
        return body
    
@app.route('/get_data', methods=['POST'])
def get_data():

    selected_currency = request.form.get("currency")
    pln_amount = request.form.get("amount")
    

    api_url = f"http://api.nbp.pl/api/exchangerates/rates/a/{selected_currency}/{format_date}/"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print(data)

        rates = data.get("rates", [])
        if rates and isinstance(rates, list):
            mid = rates[0].get("mid")
            if mid:
                result = float(pln_amount) / float(mid)
                return f"You change {pln_amount} PLN for {selected_currency}. The average stock for today or the {selected_currency} is {mid}. You receive {round(result, 2)} {selected_currency}"
            else:
                return jsonify({"error": "Mid rate not found"}), 404
        else:
            return jsonify({"error": "Rates data not found or invalid"}), 404
        
    else:
        #return jsonify({"error": "Failed to fetch data"}), response.status_code
        yesterday_url = f"http://api.nbp.pl/api/exchangerates/rates/a/{selected_currency}/{yesterday}/"
        yesterday_response = requests.get(yesterday_url)

        yesterday_data = yesterday_response.json()
        print(yesterday_data)

        yesterday_rates = yesterday_data.get("rates", [])
        if yesterday_rates and isinstance(yesterday_rates, list):
            yesterday_mid = yesterday_rates[0].get("mid")
            if yesterday_mid:
                result = float(pln_amount) / float(yesterday_mid)
                return f"""You change {pln_amount} PLN for {selected_currency}. 
                The Average stock for {yesterday} of the {selected_currency} is {yesterday_mid}.
                You receive {round(result, 2)} {selected_currency}."""
            else:
                return f"There is no data for {today} and for {yesterday}"

    
    
@app.route('/cantor', methods=['GET', 'POST'])
def cantor():

    if request.method == 'GET':
        body = f'''
            <form id="exchange_currency" action="{ url_for('cantor_exchange') }" method="POST">
                <label for="currency_one">Choose first currency</label>
                <select id="currency_one" name="currency_one">
                        <option value="eur">Euro</option>
                        <option value="usd">USD</option>
                        <option value="chf">CHF</option>
                        <option value="gbp">GBP</option>
                    </select>
                <label for="amount_one">Enter amount:</label>
                    <input type="number" id="amount_one" name="amount_one" required min="0" step="any"><br>
                <label for="currency_two">Choose second currency</label>
                <select id="currency_two" name="currency_two">
                        <option value="eur">Euro</option>
                        <option value="usd">USD</option>
                        <option value="chf">CHF</option>
                        <option value="gbp">GBP</option>
                    </select>
                    <input type="submit" value="Submit">
            </form>        
        '''
        return body

@app.route('/cantor_exchange', methods=['POST'])
def cantor_exchange():

    currency_one = request.form.get("currency_one")
    currency_two = request.form.get("currency_two")

    amount_one = request.form.get("amount_one")

    url_one = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_one}/{format_date}/"
    response_one = requests.get(url_one)

    url_two = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_two}/{format_date}/"
    response_two = requests.get(url_two)

    if response_one.status_code == 200 and response_two.status_code == 200:
        data_one = response_one.json()
        data_two = response_two.json()
        print(data_one, data_two)

        rates_one = data_one.get("rates", [])
        rates_two = data_two.get("rates", [])

        if rates_one and isinstance(rates_one, list) and rates_two and isinstance(rates_two, list):
            mid_one = rates_one[0].get("mid")
            mid_two = rates_two[0].get("mid")
            if mid_one and mid_two:
                result = (float(mid_one) * float(amount_one)) / float(mid_two)
                return f"You change {amount_one} {currency_one}. The average stock for {today} for the {currency_one} is {mid_one}PLN. You receive {round(result, 2)} {currency_two} which average stock for today is {mid_two}PLN"
            else:
                return jsonify({"error": "Mid rate not found"}), 404
        else:
            return jsonify({"error": "Rates data not found or invalid"}), 404
    else:
        #return jsonify({"error": "Failed to fetch data"}), response_one.status_code, response_two.status_code
        yesterday_url_one = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_one}/{yesterday}/"
        yesterday_response_one = requests.get(yesterday_url_one)

        yesterday_url_two = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_two}/{yesterday}/"
        yesterday_response_two = requests.get(yesterday_url_two)

        yesterday_data_one = yesterday_response_one.json()
        yesterday_data_two = yesterday_response_two.json()
        print(yesterday_data_one, yesterday_data_two)

        yesterday_rates_one = yesterday_data_one.get("rates", [])
        yesterday_rates_two = yesterday_data_two.get("rates", [])

        if yesterday_rates_one and isinstance(yesterday_rates_one, list) and yesterday_rates_two and isinstance(yesterday_rates_two, list):
            yesterday_mid_one = yesterday_rates_one[0].get("mid")
            yesterday_mid_two = yesterday_rates_two[0].get("mid")

            if yesterday_mid_one and yesterday_mid_two:
                yesterday_result = (float(yesterday_mid_one) * float(amount_one)) / float(yesterday_mid_two)
                return f"""You change {amount_one} {currency_one}.
                 The average stock price for {today} is not available yet, so price from {yesterday} will be taken. 
                 You will received {round(yesterday_result, 2)} {currency_two}"""
            else:
                return f"There is no data for {today} and for {yesterday}"


if __name__ == '__main__':
    app.run(debug=True)