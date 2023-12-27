from aiogram import executor
from database.personal_actions import dp
import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(dp.sheduler())
    executor.start_polling(dp, skip_updates=True)
