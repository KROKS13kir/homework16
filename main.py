import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

from models import *

#конфигурируем app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homebase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

#получение юзеров, работаем с methods
@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == "GET":
        res = []
        for user in User.query.all():
            res.append(user.to_dict())
        return jsonify(res)
    if request.method == "POST":
        try:
            user = json.loads(request.data)
            new_user_obj = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
            )
            db.session.add(new_user_obj)
            db.session.commit()
            db.session.close()
        except Exception as e:
            return e
    return "Пользователь создан в базе данных", 200

#получение юзера, работаем с methods
@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        if user is None:
            return "Не найдено"
        else:
            return jsonify(user.to_dict())
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден!", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.phone = user_data['phone']
        user.role = user_data['role']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()
        return f"Объект с id {user_id} успешно изменён", 200
    elif request.method == "DELETE":
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден!", 404
        db.session.delete(user)
        db.session.commit()
        return f"Объект с id {user_id} успешно удалён", 200

#получение заказов, работаем с methods
@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == "GET":
        res = []
        for order in Order.query.all():
            res.append(order.to_dict())
        return jsonify(res)
    if request.method == "POST":
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(_) for _ in order["start_date"].split("/")]
            month_end, day_end, year_end = [int(_) for _ in order["end_date"].split("/")]
            new_user_obj = Order(
                id=order['id'],
                name=order['first_name'],
                description=order['description'],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=year_end, month=month_end, day=day_end),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
            db.session.add(new_user_obj)
            db.session.commit()
            db.session.close()
        except Exception as e:
            return e
    return "Заказ создан в базе данных", 200

#получение заказа, работаем с methods
@app.route('/orders/<int:orders_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(orders_id):
    if request.method == "GET":
        order = User.query.get(orders_id)
        if order is None:
            return "Заказ не найден"
        else:
            return jsonify(order.to_dict())
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(orders_id)
        if order is None:
            return "Заказ не найден!", 404
        month_start, day_start, year_start = [int(_) for _ in order_data["start_date"].split("/")]
        month_end, day_end, year_end = [int(_) for _ in order_data["end_date"].split("/")]
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.date(year=year_end, month=month_end, day=day_end)
        order.address = order_data['address']
        order.price = order_data['price']
        order.executor_id = order_data['executor_id']
        order.customer_id = order_data['customer_id']
        db.session.add(order)
        db.session.commit()
        return f"Объект с id {orders_id} успешно изменён", 200
    elif request.method == "DELETE":
        order = db.session.query(User).get(orders_id)
        if order is None:
            return "Пользователь не найден!", 404
        db.session.delete(order)
        db.session.commit()
        return f"Объект с id {orders_id} успешно удалён", 200

#получение предложений, работаем с methods
@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == "GET":
        res = []
        for offer in Offer.query.all():
            res.append(offer.to_dict())
        return jsonify(res)
    if request.method == "POST":
        try:
            offer = json.loads(request.data)
            new_user_obj = User(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
            )
            db.session.add(new_user_obj)
            db.session.commit()
            db.session.close()
        except Exception as e:
            return e
    return "Предложение создано в базе данных", 200

#получение предложения, работаем с methods
@app.route('/offers/<int:offers_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offers_id):
    if request.method == "GET":
        offer = User.query.get(offers_id)
        if offer is None:
            return "Заказ не найден"
        else:
            return jsonify(offer.to_dict())
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = db.session.query(User).get(offers_id)
        if offer is None:
            return "Предложение не найдено!", 404
        offer.executor_id = offer_data['executor_id']
        offer.order_id = offer_data['order_id']
        db.session.add(offer)
        db.session.commit()
        return f"Объект с id {offers_id} успешно изменён", 200
    elif request.method == "DELETE":
        user = db.session.query(User).get(offers_id)
        if user is None:
            return "Пользователь не найден!", 404
        db.session.delete(user)
        db.session.commit()
        return f"Объект с id {offers_id} успешно удалён", 200


if __name__ == '__main__':
    app.run()
