from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

import sqlite3
import os


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"\tSalut, {message.from_user.full_name}! 👋 \nAcest bot este conceput pentru a vă anunța despre știrile zilnice de pe site-ul web al Martorilor lui Iehova ( jw .org ), \nBotul este în curs de dezvoltare și mă voi bucura dacă raportați funcționarea sa incorectă.😊 \n@andyrei")

    if not os.path.exists("data.db"):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE users(user_id INTEGER, username TEXT)')
        conn.close()

    list_users = await get_list_users()

    if not message.from_user.id in list_users:

        try:
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "@{message.from_user.username}")')
            conn.commit()
            conn.close()
        except Exception as e:
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
