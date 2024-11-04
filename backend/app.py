from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance

app = Flask(__name__)
CORS(app)


@app.route('/yfinance/get_price', methods=['POST'])
def get_price():
    data = request.get_json()
    symbol = data.get("ticker")
    ticker = yfinance.Ticker(symbol)
    if ticker.info['trailingPegRatio'] == None:
        return jsonify({'error':'error'}), 400
    return jsonify({'price':f"{ticker.info['currentPrice']:.2f}"}), 200

@app.route('/yfinance/get_stocks', methods=['GET'])
def get_stocks():
    tickers = yfinance.Tickers("AAPL TSLA MSFT NVDA")
    infos = []
    for symbol, ticker in tickers.tickers.items():
        data = ticker.info
        infos.append({
            "symbol":symbol,
            "name":data['shortName'],
            'price': f"{data['currentPrice']:.2f}",
            'high': data['dayHigh'],
            'low':data['dayLow'],
            'target':data['targetMeanPrice'],
            'recommendation':data['recommendationKey']
        })
    return jsonify({'infos':infos}), 200

if __name__ == '__main__':
    app.run(debug=True)