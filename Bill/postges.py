import psycopg2



class DB:
    def __init__(self, conn_props):
        sql = '''
            create table if not exists orders(
                id serial primary key,
                place_id integer,
                service float,
                total float,
                time float,
                user_id int
            );
            
            create table if not exists individuals(
                subuser_id integer,
                stuff_id integer,
                order_id integer
            );
            
            create table if not exists groups(
                stuff_id integer,
                order_id integer
            );
            
            create table if not exists stuffs(
                id serial primary key,
                name varchar,
                price float,
                place_id integer
            );
            
            create table if not exists places(
                id serial primary key,
                name varchar,
                lat float,
                lng float
            );
            
            create table if not exists users(
                id serial primary key,
                username varchar
            );
            
            create table if not exists subusers(
                id serial primary key,
                user_id integer,
                name varchar
            );
        '''
        self.__conn = None
        self.conn_props = conn_props
        self.create_connection()
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        self.close_connection()




    def create_connection(self):
        if not self.__conn:
            try:
                conn = psycopg2.connect(self.conn_props)
                self.__conn = conn
            except:
                raise ConnectionError('can not connect to database')

    def close_connection(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def newUser(self, username):
        sql = '''
            insert into users (username) values (%s)
        '''
        selectSQL = '''
            select id, username from users where username = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, (username,))

        cursor.execute(selectSQL, (username,))

        createdUser = cursor.fetchone()
        cursor.close()
        conn.commit()

        return dict(id=createdUser[0], username=createdUser[1])

    def getUserByUsername(self, username):
        sql = '''
            select id, username from users where username = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return dict(id=user[0], username=user[1])
        else:
            return None

    def getSubusersByUserid(self, user_id):
        sql = '''
            select id, user_id, name from subusers where user_id = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        users = cursor.fetchall()
        cursor.close()
        subusers = []
        for subuser in users:
            subusers.append(dict(
                id=subuser[0],
                user_id=subuser[1],
                name=subuser[2]
            ))
        return subusers

    def getSubuser(self, subuser_id, user_id):
        sql = '''
            select id, user_id, name from subusers where id = %s and user_id = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, (subuser_id, user_id))
        subuser = cursor.fetchone()
        print(subuser_id, user_id)
        print(subuser)
        if not subuser:
            return None
        return dict(id=subuser[0], user_id=subuser[1], name=subuser[2])

    def getSubuserName(self, subuser_id, user_id):
        sql = '''
            select name from subusers where id = %s and user_id = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, (subuser_id, user_id))
        subuser = cursor.fetchone()
        if not subuser:
            return None
        return subuser[0]

    def newSubuser(self, user_id, name):
        sql = '''
            insert into subusers (user_id, name) values(%s, %s)
        '''
        sql2 = '''
            select id, user_id, name from subusers where user_id = %s and name = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, name))
        cursor.execute(sql2, (user_id, name))
        subuser = cursor.fetchone()
        cursor.close()
        conn.commit()
        return dict(id=subuser[0], user_id=subuser[1], name=subuser[2])

    def delSubuser(self, user_id, id):
        sql = '''
            delete from subusers where user_id = %s and id = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (user_id, id))
            ok = 1
        except:
            ok = 0
        cursor.close()
        conn.commit()
        return ok

    def delStuff(self, id):
        sql = '''
            delete from stuffs where id = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (id,))
            ok = 1
        except:
            ok = 0
        cursor.close()
        conn.commit()
        return ok

    def delPlace(self, id):
        sql = '''
            delete from places where id = %s
        '''
        conn = self.__conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (id,))
            ok = 1
        except:
            ok = 0
        cursor.close()
        conn.commit()
        return ok

    def newStuff(self, name, price, place_id):
        sql = '''
            insert into stuffs(name, price, place_id) values (%s, %s, %s)
        '''
        sql2 = '''
            select id, name, price, place_id from stuffs where name=%s and price=%s and place_id=%s
        '''
        conn = self.__conn
        params = (name, price, place_id)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        cursor.execute(sql2, params)
        stuff = cursor.fetchone()
        cursor.close()
        conn.commit()
        return dict(id=stuff[0], name=stuff[1], price=stuff[2], place_id=stuff[3])

    def stuffList(self, place_id):
        sql = '''
            select id, name, price, place_id from stuffs where place_id=%s
        '''
        conn = self.__conn
        params = (place_id,)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        stuffs = cursor.fetchall()
        cursor.close()
        l = []
        for stuff in stuffs:
            l.append(dict(
                id=stuff[0],
                name=stuff[1],
                price=stuff[2],
                place_id=stuff[3]
            ))
        return l

    def getStuff(self, id, place_id):
        sql = '''
            select id, name, price, place_id from stuffs where id=%s and place_id = %s
        '''
        conn = self.__conn
        params = (id, place_id)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        stuff = cursor.fetchone()
        cursor.close()
        if not stuff:
            return None
        return dict(id=stuff[0],
                    name=stuff[1],
                    price=stuff[2],
                    place_id=stuff[3])

    def newPlace(self, name, lat=0, lng=0):
        sql = '''
            insert into places(name, lat, lng) values (%s, %s, %s)
        '''
        sql2 = '''
            select id, name, lat, lng from places where name=%s and lat=%s and lng=%s
        '''
        conn = self.__conn
        params = (name, lat, lng)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        cursor.execute(sql2, params)
        place = cursor.fetchone()
        cursor.close()
        conn.commit()
        return dict(id=place[0], name=place[1])

    def placeList(self):
        sql = '''
            select id, name, lat, lng from places 
        '''
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql)
        places = cursor.fetchall()
        cursor.close()
        l = []
        for place in places:
            l.append(dict(
                id=place[0],
                name=place[1]
            ))
        return l

    def newOrder(self, place_id, service, total, time, user_id):
        sql = '''
            insert into orders (place_id, service, total, time, user_id) values(%s, %s, %s, %s, %s)
        '''
        sql2 = '''
            select 
                id, place_id, service, total, user_id
            from orders 
            where 
                place_id = %s and 
                service = %s and 
                total = %s and
                time = %s and
                user_id = %s
        '''
        params = (place_id, service, total, time, user_id)
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, params)
        cursor.execute(sql2, params)
        order = cursor.fetchone()
        cursor.close()
        conn.commit()

        return dict(id=order[0],
                    place_id=order[1],
                    service=order[2],
                    total=order[3],
                    user_id=order[4])

    def newIndividual(self, subuser_id, stuff_id, order_id):
        sql = '''
            insert into individuals(
                subuser_id, stuff_id, order_id) 
            values(%s, %s, %s)
        '''
        sql2 = '''
            select 
                subuser_id, stuff_id, order_id
            from individuals 
            where 
                subuser_id = %s and 
                stuff_id = %s and 
                order_id = %s
        '''
        params = (subuser_id, stuff_id, order_id)
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, params)
        cursor.execute(sql2, params)
        indiv = cursor.fetchone()
        cursor.close()
        conn.commit()

        return dict(subuser_id=indiv[0],
                    stuff=indiv[1],
                    order_id=indiv[2])

    def newGroup(self, stuff_id, order_id):
        sql = '''
            insert into groups (stuff_id, order_id) values(%s, %s)
        '''
        sql2 = '''
            select 
                stuff_id, order_id
            from groups 
            where 
                stuff_id = %s and 
                order_id = %s 
        '''
        params = (stuff_id, order_id)
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql, params)
        cursor.execute(sql2, params)
        group = cursor.fetchone()
        cursor.close()
        conn.commit()

        return dict(stuff_id=group[0], order_id=group[1])
