import keyboard
import sqlite3
from datetime import datetime
from tracker.utils import is_a_special_char

def create_db_tables():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dates
                      (id INTEGER PRIMARY KEY, date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS keyboard
                      (id INTEGER PRIMARY KEY, dates_id INTEGER, FOREIGN KEY(dates_id) REFERENCES dates(id))''')
    connection.commit()
    connection.close()

def check_if_date_exists(date):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM dates WHERE date = ?", (date,))
    result = cursor.fetchone()
    id = None

    if result:
        id = result[0]
    else:
        cursor.execute("INSERT INTO dates (date) VALUES (?)", (date,))
        id = cursor.lastrowid

    connection.commit()
    connection.close()
    return id

def add_keypress_frequecy(key_name, date_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    cursor.execute(f"PRAGMA table_info(keyboard)")
    columns = [column[1] for column in cursor.fetchall()]
    if key_name.isdigit() or is_a_special_char(key_name):
            key_name = f"key_{key_name}"
            print(key_name)
   
    if key_name not in columns:
        cursor.execute(f"ALTER TABLE keyboard ADD COLUMN \"{key_name}\" INTEGER DEFAULT 0")

    cursor.execute("SELECT COUNT(*) FROM keyboard WHERE dates_id = ?", (date_id,))
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        cursor.execute("INSERT INTO keyboard (dates_id) VALUES (?)", (date_id,))

    cursor.execute(f"UPDATE keyboard SET \"{key_name}\" = \"{key_name}\" + 1 WHERE dates_id = ?", (date_id,))

    connection.commit()
    connection.close()
    return 'updated'

def key_press(event):
    if event.name == 'space' or event.name == 'enter':
        return
    
    date = datetime.now().date() # returns in formart 2024-05-07
    
    id = check_if_date_exists(str(date))

    add_keypress_frequecy(event.name, id)
    

create_db_tables()

keyboard.on_press(key_press)

keyboard.wait('esc')