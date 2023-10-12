#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = None

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()

    bakery_list = [
        {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at
        }
        for bakery in bakeries
    ]
    return jsonify(bakery_list), 200

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.get(id)

    if bakery:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.isoformat() if bakery.created_at else None,
            'updated_at': bakery.updated_at.isoformat() if bakery.updated_at else None,
            'baked_goods': [
                {
                    'id': good.id,
                    'name': good.name,
                    'price': good.price,
                    'created_at': good.created_at.isoformat() if good.created_at else None,
                    'updated_at': good.updated_at.isoformat() if good.updated_at else None
                } 
                for good in bakery.baked_goods
            ]
        }
        return jsonify(bakery_data), 200
    else:
        return jsonify({'message': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    guuds= BakedGood.query.order_by(BakedGood.price.desc()).all()
    new_array=[guud.to_dict() for guud in guuds]
    return jsonify(new_array), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive_good:
        most_expensive_data = most_expensive_good.to_dict()
        return make_response(most_expensive_data, 200)
    else:
        return jsonify({'message': 'No baked goods found.'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    print(f'The thing I need: {jsonify(baked_goods_list), 200}')