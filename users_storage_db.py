import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return bool(len(result.fetchall()))

    def add_user(self, user_id, full_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))

    def user_ban(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET ban = 1 WHERE user_id = ?", (user_id,))
            self.connection.commit()

    def user_un_ban(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET ban = 0 WHERE user_id = ?", (user_id,))
            self.connection.commit()

    def set_block(self, user_id, block):
        try:
            with self.connection:
                return self.cursor.execute("UPDATE users SET block = ? WHERE user_id = ?", (block, user_id,))
        except sqlite3.Error as e:
            print("Ошибка SQLite:", e)

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, block FROM users").fetchall()

    def check_ban_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT ban FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if result and result[0] == 1:
                return True
            else:
                return False

    def delete_user(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    def get_blocked_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id, full_name FROM users WHERE ban = 1").fetchall()
            blocked_users = [{"user_id": row[0], "full_name": row[1]} for row in result]
            return blocked_users

    def get_unblocked_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id, full_name FROM users WHERE ban = 0").fetchall()
            blocked_users = [{"user_id": row[0], "full_name": row[1]} for row in result]
            return blocked_users

    def user_count(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            result = self.cursor.fetchone()
            return result[0]

    def user_list_balans(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id, full_name, money FROM users").fetchall()
            users = []
            for row in result:
                user = {"user_id": row[0], "full_name": row[1], "money": row[2]}
                users.append(user)
            return users
