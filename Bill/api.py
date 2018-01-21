from Bill.dataBase import DB
from Bill import db
from math import ceil
from time import time
# ['place_id', 'service', 'individuals', 'group', 'users', 'user_id']


def getBill(data):
    db.create_connection()
    total = 0
    group_total = 0
    userscnt = len(data['users'])
    service = data['service'] / 100
    place_id = data['place_id']
    user_id = data['user_id']

    for item in data['group']:
        stuff = db.getStuff(item, place_id)
        if not stuff:
            print('stuff {} not found'.format(item))
            continue
        group_total += stuff['price'] + stuff['price'] * service
    userTotal = group_total / userscnt
    individ = dict()

    for item in data['individuals']:
        subuser_id = item['user_id']
        stuff_id = item['stuff_id']
        utotal = individ.get(subuser_id, 0)
        stuff = db.getStuff(stuff_id, place_id)
        if not stuff:
            print('stuff {} not found'.format(stuff_id))
            continue
        utotal += stuff['price'] + stuff['price'] * service
        individ[subuser_id] = utotal

    l = []
    for user in data['users']:
        ind = individ.get(user, 0)
        pay = dict(name=db.getSubuserName(user, user_id))
        pay['total'] = ceil(userTotal + ind)
        total += pay['total']
        l.append(pay)
    order = db.newOrder(place_id, data['service'], total, int(time()), user_id)
    for i in data['individuals']:
        db.newIndividual(i['user_id'], i['stuff_id'], order['id'])
    for i in data['group']:
        db.newGroup(i, order['id'])
    db.close_connection()
    return dict(total=total, individuals=l)


def delStuff(id):
    db.create_connection()
    ok = db.delStuff(id)
    db.close_connection()
    return ok


def delSubuser(user_id, id):
    db.create_connection()
    ok = db.delSubuser(user_id, id)
    db.close_connection()
    return ok


def delPlace(id):
    db.create_connection()
    ok = db.delPlace(id)
    db.close_connection()
    return ok


def register(username):
    user = None
    db.create_connection()
    found = db.getUserByUsername(username)
    if not found:
        user = db.newUser(username)
    db.close_connection()
    return user


def login(username):
    db.create_connection()
    user = db.getUserByUsername(username)
    db.close_connection()
    return user


def newSubuser(user_id, name):
    db.create_connection()
    subuser = db.newSubuser(user_id, name)
    db.close_connection()
    return subuser


def subUsersList(user_id):
    db.create_connection()
    subusers = db.getSubusersByUserid(user_id)
    db.close_connection()
    return subusers


def newPlace(name):
    db.create_connection()
    place = db.newPlace(name, 0, 0)
    db.close_connection()
    return place


def placeList():
    db.create_connection()
    plist = db.placeList()
    db.close_connection()
    return plist


def newStuff(name, price, place_id):
    db.create_connection()
    stuff = db.newStuff(name, price, place_id)
    db.close_connection()
    return stuff


def stuffList(place_id):
    db.create_connection()
    slist = db.stuffList(place_id)
    db.close_connection()
    return slist




