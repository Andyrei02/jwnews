from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

import asyncio
import aioschedule
import news_parser
import json
import os
from aiogram import types
import sqlite3



# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"{message.text}")

async def parse_news(dp):
    
    dict_last_news = await news_parser.parse()

    if not os.path.exists("last_news.json"):
        with open("last_news.json", "w") as f:
            f.write(json.dumps('{}'))

    with open("last_news.json", "r") as f:
        dict_previous_news = json.loads(f.read())

    if not dict_previous_news == dict_last_news:
        with open("last_news.json", "w") as f:
            f.write(json.dumps(dict_last_news))

        await send_post(dict_last_news)


async def send_post(news):
    title = news["title"]
    link = news["url"]
    intro = news["intro"]

    caption = f"<b>{title}</b>\n{intro}...\n<a href='{link}'>open article</a>"
    list_users = await get_profile()
    
    for user in list_users:
        await dp.bot.send_photo(user, caption=caption, photo=link, parse_mode="HTML")

async def scheduler(dp):
    try:
        aioschedule.every(60).seconds.do(parse_news, dp)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except:
        pass


async def get_profile():
    if not os.path.exists("data.db"):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE users(user_id INTEGER, username TEXT)')
        conn.close()

    conn = sqlite3.connect('data.db')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users')
    result = cur.fetchall()
    
    conn.close()
    return result


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
