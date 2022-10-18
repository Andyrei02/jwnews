from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

import sqlite3
import os


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!")

    if not os.path.exists("data.db"):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE users(user_id INTEGER, username TEXT)')
        conn.close()

    list_users = await get_list_users()
    if not message.from_user.username in list_users:

        try:
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "@{message.from_user.username}")')
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
            conn.commit()
            conn.close()

async def get_list_users():
    conn = sqlite3.connect('data.db')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users')
    result = cur.fetchall()
    
    conn.close()
    return result
