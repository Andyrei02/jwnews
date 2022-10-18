from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from handlers.users.post import scheduler
import asyncio


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    asyncio.create_task(scheduler(dispatcher))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

