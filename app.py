from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
import dbm


app = Flask(__name__)


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/<code>')
def code(code):

    return render_template('home.html', code=code)


@app.route('/<code>/send', methods=['POST'])
def send(code):

    data = request.get_json()['data']
    os.environ["tmp"] = data

    with dbm.open('db_store', 'c') as db:
        db[code] = data

    return jsonify({
        'last_updated': '',
        'data': data
    })


@app.route('/<code>/receive')
def receive(code):

    try:
        with dbm.open('db_store', 'c') as db:
            data = db[code].decode("utf-8")
    except KeyError:
        data = ''

    print('DATA HERE')
    print(data)

    return jsonify({
        'last_updated': '',
        'data': data
    })


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

    return (division_by_zero)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
