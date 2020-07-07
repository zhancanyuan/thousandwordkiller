import pymysql

# import pandas as pd


class mysqlsearch():
    def __init__(self):
        self.get_connect()

    # 获取连接
    def get_connect(self):
        try:
            self.conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                passwd='root',
                db='test',
                charset='utf8'
            )
        except pymysql.Error as e:
            print('Error:%s ' % e)

    # 关闭连接
    def close_connect(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print('Error: %s' % e)

    # 获取用户信息（登陆用）
    def get_userinfo(self):
        sql = 'SELECT * FROM usr'
        # 使用cursor()方法获取操作游标
        cursor = self.conn.cursor()
        # 使用execute()方法执行SQL语句
        cursor.execute(sql)
        # 使用fetchall()方法获取全部数据
        result = cursor.fetchall()
        # 将数据用字典形式存储与result
        result = [dict(zip([k[0] for k in cursor.description], row)) for row in result]
        # 关闭连接
        cursor.close()
        self.close_connect()
        return result

    def get_default_user(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM usr')
        res = cursor.fetchone()
        return res

    # 注册
    def insert_userinfo(self, a, b):
        self.a = a
        self.b = b
        if self.a == '' or self.b == '':
            self.conn.rollback()
            return 1  # 1表示空用户名或密码
        sql = 'SELECT * FROM usr'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [dict(zip([k[0] for k in cursor.description], row)) for row in result]
        ulist = []
        for item in result:
            ulist.append(item['usrname'])
        try:
            # sql = 'INSERT INTO usr(usrname,password) VALUES(%s,%s)'
            cursor = self.conn.cursor()
            num = cursor.execute('select * from usr')
            cursor.execute('INSERT INTO usr(id,usrname,password,killedwords) VALUES(%s,%s,%s,%s)',
                           (num + 1, self.a, self.b, 0))
            if self.a in ulist:
                # messagebox.showerror('警告', message='用户名已存在')
                return 2  # 2表示用户已存在
            else:
                # 提交事务
                self.conn.commit()
                # messagebox.showinfo(title='恭喜', message='注册成功')
                print("ok!")
                return 3  # 3表示成功
            cursor.close()
            self.close_conn()
        except:
            # 限制提交
            self.conn.rollback()
            print("error")
            return 4


if __name__ == "__main__":
    sq = mysqlsearch()
    cursor = sq.conn.cursor()
    sql = 'SELECT * FROM usr'

    # 使用execute()方法执行SQL语句
    cursor.execute(sql)

    # 使用fetchall()方法获取全部数据
    result = cursor.fetchall()

    # 将数据用字典形式存储与result
    result = [dict(zip([k[0] for k in cursor.description], row)) for row in result]
    ul = []
    pl = []
    print(result)
    cursor.close()
    for r in result:
        ul.append(r['usrname'])

    print(ul)
