import mysql.connector

def connect_to_db():
   return mysql.connector.connect(user='root', password='root',
                                 database='webappmenu', host='127.0.0.1')

# Проверка есть пользователь в БД или нет
def check_user_id_in_db(user_id):
   conn = connect_to_db()
   cursor = conn.cursor(buffered=True)
   try:
      cursor.execute(f'SELECT * FROM users WHERE `UserId` = {user_id}')
      result = cursor.fetchone()
      return result is not None
   finally:
      cursor.close()
      conn.close()

# Добавление пользователя в БД
def insert_user_id_in_db(user_id, phone_number):
   conn = connect_to_db()
   cursor = conn.cursor(buffered=True)
   try:
      cursor.execute(f'INSERT INTO users (`UserId`, `PhoneNumber`) VALUES ({user_id}, {phone_number})')
      conn.commit()
      return True
   finally:
      cursor.close()
      conn.close()

# Проверка есть пользователь в БД в таблице `администраторы` или нет
def check_admin_in_db(user_id):
   conn = connect_to_db()
   cursor = conn.cursor(buffered=True)
   try:
      cursor.execute(f'SELECT * FROM admins WHERE `UserId` = {user_id}')
      result = cursor.fetchone()
      return result is not None
   finally:
      cursor.close()
      conn.close()

# Добавление пользователя в БД в таблицу `администраторы`
def insert_admin_in_db(user_id):
   conn = connect_to_db()
   cursor = conn.cursor(buffered=True)
   cursor.execute('SELECT COUNT(*) FROM admins')
   if (cursor.fetchone()[0] <= 2):
      try:
         cursor.execute(f'INSERT INTO admins (`UserId`, `NumberPhone`) SELECT `UserId`, `NumberPhone` FROM users WHERE `UserId` = {user_id}')
         conn.commit()
         return True
      finally:
         cursor.close()
         conn.close()
   else:
      return False