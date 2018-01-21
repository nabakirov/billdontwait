from Bill import app, api
from Bill.utils import getargs
from flask import request, abort, jsonify


@app.route('/api/login', methods=['POST', 'GET'])
def login():
    username = getargs(request, 'username')[0]
    if not username:
        return abort(400)
    user = api.login(username)
    if not user:
        return abort(404)
    return jsonify(user)


@app.route('/api/register', methods=['POST', 'GET'])
def register():
    username = getargs(request, 'username')[0]
    if not username:
        return abort(400)

    user = api.register(username)
    if not user:
        return 'user already exists', 500

    return jsonify(user)


@app.route('/api/place', methods=['POST', 'GET', 'DELETE'])
def place_handler():
    if request.method == 'POST':
        name = getargs(request, 'name')[0]
        if not name:
            return abort(400)
        place = api.newPlace(name)
        return jsonify(place)
    elif request.method == 'DELETE':
        id = getargs(request, 'id')[0]
        if not id:
            return abort(400)
        ok = api.delPlace(id)
        if ok:
            return 'ok', 200
        else:
            return abort(500)
    places = api.placeList()
    return jsonify(places)


@app.route('/api/subuser', methods=['POST', 'GET', 'DELETE'])
def subuser_handler():
    if request.method == 'POST':
        user_id, name = getargs(request, 'user_id', 'name')
        if not user_id or not name:
            return abort(400)
        subuser = api.newSubuser(user_id, name)
        return jsonify(subuser)
    elif request.method == 'DELETE':
        user_id, id = getargs(request, 'user_id', 'id')
        if not user_id or not id:
            return abort(400)
        ok = api.delSubuser(user_id, id)
        if ok:
            return 'ok', 200
        return abort(500)
    user_id = getargs(request, 'user_id')[0]
    if not user_id:
        return abort(400)
    subusers = api.subUsersList(user_id)
    return jsonify(subusers)


@app.route('/api/stuff', methods=['POST', 'GET', 'DELETE'])
def stuff_handler():
    if request.method == 'POST':
        name, price, place_id = getargs(request, 'name', 'price', 'place_id')
        if not name or not price or not place_id:
            return abort(400)
        stuff = api.newStuff(name, price, place_id)
        return jsonify(stuff)
    elif request.method == 'DELETE':
        id = getargs(request, 'id')[0]
        if not id:
            return abort(400)
        ok = api.delStuff(id)
        if ok:
            return 'ok', 200
        return abort(500)
    place_id = getargs(request, 'place_id')[0]
    if not place_id:
        return abort(400)

    stuffs = api.stuffList(place_id)
    return jsonify(stuffs)


@app.route('/api/order', methods=['POST'])
def order_handler():
    data = request.get_json(force=True, silent=True)
    required = ['place_id', 'service', 'individuals', 'group', 'users', 'user_id']
    for r in required:
        if r not in data:
            return abort(400)

    bill = api.getBill(data)

    return jsonify(bill)


