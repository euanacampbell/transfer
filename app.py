from flask import Flask, render_template, redirect, url_for, request, jsonify
import dbm
import uuid

from modules.helper_functions import get_expiry, date_to_string
from modules.db import Code


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    code = request.args.get('code') or uuid.uuid4().hex[0:6]

    return render_template('home.html', code=Code(code.upper()))


@app.route('/sys/codes')
def keys():

    with dbm.open('db_store', 'c') as db:
        all_keys = db.keys()

    all_codes = [key.decode("utf-8") for key in all_keys]

    return render_template('keys.html', codes=all_codes)


@app.route('/<code>')
def code(code):

    return render_template('code.html', code=Code(code))


@app.route('/<code>/send', methods=['POST'])
def send(code):

    response = request.get_json()

    code_data = {
        'clipboard': response['clipboard'],
        'expiry': date_to_string(get_expiry(response['expiry_option']))
    }

    Code(code).add(code_data)

    return jsonify(code_data)


@app.route('/<code>/receive')
def receive(code):

    data = Code(code).clipboard

    return jsonify({
        'clipboard': data
    })


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

    return (division_by_zero)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
