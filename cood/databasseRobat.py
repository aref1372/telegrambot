#-*- coding: utf-8 -*-

import psycopg2


# اطلاعات اتصال به دیتابیس
DB_NAME = "TelegramBotIR98"
DB_USER = "bot-ir-98"
DB_PASSWORD = "13729322!!"
DB_HOST = "localhost"
DB_PORT = "5432"  # پورت پیش‌فرض PostgreSQL


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(" verbindung an databasse war erfolgreich")
        return conn
    except Exception as e:
        print(f" gibt problem für verbindung an databasse : {e}")
        return None
    

    # این یک تابع است برای ایجاد جدول

def create_table():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tabelle ist erfolgreich erstellt ")



#if __name__ == "__main__":
    #create_table()




# تابع ای برای ‌ذخییره اطلاعات کاربر

def add_user(telegram_id, username, full_name):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO users (telegram_id, username, full_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (telegram_id) DO NOTHING;
            ''', (telegram_id, username, full_name))
            conn.commit()
            print(f" user {full_name} erfolgreich user hinzugefügt")
        except Exception as e:
            print(f" problem für user hinzufügen {e}")
        finally:
            cur.close()
            conn.close()
