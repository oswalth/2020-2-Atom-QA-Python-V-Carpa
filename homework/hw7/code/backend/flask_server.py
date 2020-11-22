import json

from flask import Flask, jsonify, redirect, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from backend.settings import users, products

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/logout')
@auth.login_required()
def logout():
    return f"{auth.current_user()} , bye", 401


@app.route('/profile')
@auth.login_required()
def profile():
    return f"Hello, {auth.current_user()}"


@app.route('/')
def index():
    return jsonify(products)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':
        return "Адрес: вулиця Банкова, 11, Київ, Украина, 01220"
    elif request.method == 'POST':
        data = json.loads(request.data)
        name = auth.current_user() or data.get('name', None) or 'Анонім'
        return f"{name}, ваш запит обробляється"


@app.route('/products/<int:prod_id>')
def product(prod_id):
    item = next((item for item in products if item['id'] == prod_id), None)
    if item:
        return jsonify(item)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=False, port=5555)
