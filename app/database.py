import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'fitness_club.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            duration_days INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            subscription_id INTEGER NOT NULL,
            purchase_date TEXT NOT NULL,
            expiry_date TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(subscription_id) REFERENCES subscriptions(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            trainer_name TEXT NOT NULL,
            training_time TEXT NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')

    conn.commit()
    conn.close()

    fill_initial_subscriptions()

def fill_initial_subscriptions():
    # Добавляем начальные абонементы, если их нет
    if get_all_subscriptions():
        return
    add_subscription("Абонемент на 1 месяц", 2000, 30)
    add_subscription("Абонемент на 3 месяца", 5500, 90)
    add_subscription("Индивидуальные тренировки", 5000, None)
    add_subscription("Тренировки с тренером (1 занятие)", 700, 1)

def add_client(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return client_id

def get_client_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM clients WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_subscription(name, price, duration_days):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO subscriptions (name, price, duration_days) VALUES (?, ?, ?)',
                   (name, price, duration_days))
    conn.commit()
    sub_id = cursor.lastrowid
    conn.close()
    return sub_id

def get_all_subscriptions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price, duration_days FROM subscriptions')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_purchase(client_id, subscription_id):
    purchase_date = datetime.now()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT duration_days FROM subscriptions WHERE id = ?', (subscription_id,))
    row = cursor.fetchone()
    duration = row[0] if row else None
    expiry_date = (purchase_date + timedelta(days=duration)) if duration else None
    cursor.execute('''
        INSERT INTO purchases (client_id, subscription_id, purchase_date, expiry_date)
        VALUES (?, ?, ?, ?)
    ''', (client_id, subscription_id, purchase_date.isoformat(), expiry_date.isoformat() if expiry_date else None))
    conn.commit()
    purchase_id = cursor.lastrowid
    conn.close()
    return purchase_id

def get_purchases_by_client(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, s.name, s.price, p.purchase_date, p.expiry_date
        FROM purchases p
        JOIN subscriptions s ON p.subscription_id = s.id
        WHERE p.client_id = ?
    ''', (client_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_training(client_id, trainer_name, training_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trainings (client_id, trainer_name, training_time)
        VALUES (?, ?, ?)
    ''', (client_id, trainer_name, training_time))
    conn.commit()
    training_id = cursor.lastrowid
    conn.close()
    return training_id

def get_trainings_by_client(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT trainer_name, training_time FROM trainings
        WHERE client_id = ?
    ''', (client_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_clients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM clients')
    rows = cursor.fetchall()
    conn.close()
    return rows
def get_all_purchases():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM purchases')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_trainings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trainings')
    rows = cursor.fetchall()
    conn.close()
    return rows
def cancel_purchase(purchase_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM purchases WHERE id = ?', (purchase_id,))
    conn.commit()
    conn.close()
