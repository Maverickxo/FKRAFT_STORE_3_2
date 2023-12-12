from connect_bd import connect_data_b
import psycopg2


class Database:
    def __init__(self, ):
        self.connection, self.cursor = connect_data_b()

    def user_exists(self, user_id):  # TODO Готов
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            return bool(len(result))

    def add_user(self, user_id, full_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, full_name) VALUES (%s, %s)", (user_id, full_name))

    def user_ban(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET ban = 1 WHERE user_id = %s", (user_id,))
            self.connection.commit()

    def user_un_ban(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET ban = 0 WHERE user_id = %s", (user_id,))
            self.connection.commit()

    def set_block(self, user_id, block):
        try:
            with self.connection:
                return self.cursor.execute("UPDATE users SET block = %s WHERE user_id = %s", (block, user_id,))
        except psycopg2.Error as e:
            print("Ошибка PostgreSQL:", e)

    def get_users(self):
        with self.connection:
            self.cursor.execute("SELECT user_id, block FROM users")
            result = self.cursor.fetchall()
            return result

    def check_ban_status(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT ban FROM users WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchone()
            if result and result[0] == 1:
                return True
            else:
                return False

    def delete_user(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

    def get_blocked_users(self):
        with self.connection:
            self.cursor.execute("SELECT user_id, full_name FROM users WHERE ban = 1")
            result = self.cursor.fetchall()
            blocked_users = [{"user_id": row[0], "full_name": row[1]} for row in result]
            return blocked_users

    def get_unblocked_users(self):
        with self.connection:
            self.cursor.execute("SELECT user_id, full_name FROM users WHERE ban = 0")
            result = self.cursor.fetchall()
            blocked_users = [{"user_id": row[0], "full_name": row[1]} for row in result]
            return blocked_users

    def user_count(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            result = self.cursor.fetchone()
            return result[0]

    def user_list_balans(self):
        with self.connection:
            users = []
            self.cursor.execute("SELECT user_id, full_name, money FROM users")
            result = self.cursor.fetchall()
            for row in result:
                # users = [{"user_id": row[0], "full_name": row[1], "money": row[2]} for row in result]
                user = {"user_id": row[0], "full_name": row[1], "money": row[2]}
                users.append(user)
            return users
