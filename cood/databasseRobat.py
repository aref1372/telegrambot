# databasseRobat.py
#-*- coding: utf-8 -*-

import psycopg2

# اطلاعات اتصال به دیتابیس
DB_NAME = "TelegramBotIR98"
DB_USER = "bot-ir-98"
DB_PASSWORD = "13729322!!"
DB_HOST = "localhost"
DB_PORT = "5432"  # پورت پیش‌فرض PostgreSQL

class DatabaseManager:
    def __init__(self):
        self.conn = self.connect_db()
        self.create_tables()

    def connect_db(self):
        """ اتصال به دیتابیس """
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("✅ Verbindung zur Datenbank war erfolgreich!")
            return conn
        except Exception as e:
            print(f"❌ Fehler bei der Verbindung zur Datenbank: {e}")
            return None

    def create_tables(self):
        # ایجاد جداول مورد نیاز در دیتابیس 
        if self.conn:
            cur = self.conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    username TEXT,
                    full_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS marketers (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    username TEXT,
                    full_name TEXT,
                    national_id TEXT UNIQUE NOT NULL,
                    phone_number TEXT NOT NULL,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    marketer_id BIGINT REFERENCES marketers(telegram_id) ON DELETE CASCADE,
                    product_name TEXT NOT NULL,
                    price TEXT NOT NULL,
                    description TEXT,
                    packaging TEXT,
                    image_url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            self.conn.commit()
            cur.close()
            print("✅ Tabellen erfolgreich erstellt!")

    def add_user(self, telegram_id, username, full_name):
        # افزودن کاربر جدید به دیتابیس 
        if self.conn:
            cur = self.conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO users (telegram_id, username, full_name)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (telegram_id) DO NOTHING;
                ''', (telegram_id, username, full_name))
                self.conn.commit()
                print(f"✅ User {full_name} erfolgreich hinzugefügt")
            except Exception as e:
                print(f"❌ Problem beim Hinzufügen des Users: {e}")
            finally:
                cur.close()

    def add_marketer(self, telegram_id, username, full_name, national_id, phone_number, location):
        # ثبت بازاریاب جدید 
        if self.conn:
            cur = self.conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO marketers (telegram_id, username, full_name, national_id, phone_number, location)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (telegram_id) DO NOTHING;
                ''', (telegram_id, username, full_name, national_id, phone_number, location))
                self.conn.commit()
                print(f"✅ Bazaryab {full_name} erfolgreich hinzugefügt")
            except Exception as e:
                print(f"❌ Error: Bazaryab kann nicht hinzugefügt werden: {e}")
            finally:
                cur.close()

    def add_product(self, marketer_id, product_name, price, description, packaging, image_url):
        # اضافه کردن محصول جدید برای بازاریاب 
        if self.conn:
            cur = self.conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO products (marketer_id, product_name, price, description, packaging, image_url)
                    VALUES (%s, %s, %s, %s, %s, %s);
                ''', (marketer_id, product_name, price, description, packaging, image_url))
                self.conn.commit()
                print(f"✅ Produkt {product_name} ist erfolgreich hinzugefügt")
            except Exception as e:
                print(f"❌ Error: Produkt kann nicht hinzugefügt werden: {e}")
            finally:
                cur.close()

    def get_all_marketers(self):
        # دریافت لیست تمام بازاریاب‌ها 
        if self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT telegram_id FROM marketers")
            marketers = cur.fetchall()
            cur.close()
            return [m[0] for m in marketers]  # فقط آی‌دی تلگرام را برمی‌گرداند
        return []

# ایجاد یک نمونه از دیتابیس برای استفاده در برنامه اصلی
db_manage = DatabaseManager()