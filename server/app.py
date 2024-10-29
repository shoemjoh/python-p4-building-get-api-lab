#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    print(bakeries)
    bl = []
    for bakery in bakeries:
        bl.append(bakery.to_dict())
    
    return bl, 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery:
        body = bakery.to_dict()
        status = 200
    else:
        body = {'message': f'Bakery {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    print(baked_goods)

    return [baked_good.to_dict() for baked_good in baked_goods], 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()


    if baked_good:
        body = baked_good.to_dict()
        status = 200
    else:
        body = {'message': f'Baked good not found.'}
        status = 404

    return make_response(body, status)
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
