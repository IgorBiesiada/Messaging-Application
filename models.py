from clcrypto import hash_password

class User():
    def __init__(self, username="", password="",  salt=""):
        self.username = username
        self._id = -1
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO users (username, hashed_password, ) VALUES (%s, %s) RETURNING id"
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE users SET username=%s, hashed_password=$s WHERE id=%s"
            values = (self.username, self.hashed_password, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE usename = %s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            _id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = _id
            loaded_user.hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, _id):
        sql = "SELECT id, username, hashed_password FROM users WHERE id = %s"
        cursor.execute(sql, (_id,))
        data = cursor.fetchone()
        if data:
            _id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = _id
            loaded_user.hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            _id, username, hashed_password = row
            loaded_user = User(username)
            loaded_user._id = _id
            loaded_user.hashed_password = hashed_password
            users.append(loaded_user)
        return users


    def delete(self, cursor):
        sql = "DELETE FROM user WHERE id = %s"
        cursor.execute(sql, (self._id))
        self._id = -1
        return True

class Messages():

    def __init__(self,from_id="", to_id="", text=""):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def creation_date(self):
        return self.creation_date

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO Messages from_id, to_id, text, VALUES (%s, %s, %s,) RETURNING id, creation_date"
            values = (self.from_id, self.to_id, self.text,)
            cursor.execute(sql, values)
            self._id, self.creation_date = cursor.fetchone()
            return True
        else:
            sql = "UPDATE Messages SET from_id = %s, to_id = %s, text = %s WHERE id=%s "
            values = (self.from_id, self.to_id, self.text, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            id, from_id, to_id, text, creation_date = row
            loaded_message = Messages(from_id, to_id, text)
            loaded_message._id = id
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages
