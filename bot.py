from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import logging
from config import TOKEN
import db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db.add_user(message.from_user.username, message.chat.id)
    await message.reply("Welcome! You have been added to the database.")

@dp.message_handler(commands=['begin'])
async def begin_work(message: types.Message):
    user_id = message.from_user.id
    db.start_work_session(user_id)
    await message.reply("Work session started.")

@dp.message_handler(commands=['end'])
async def end_work(message: types.Message):
    user_id = message.from_user.id
    db.end_work_session(user_id)
    worked_time = db.calculate_worked_time(user_id)
    hours = worked_time // 3600
    minutes = (worked_time % 3600) // 60
    await message.reply(f"Work session ended. Total worked time: {int(hours)} hours and {int(minutes)} minutes.")

@dp.message_handler(commands=['pause'])
async def pause_work(message: types.Message):
    user_id = message.from_user.id
    db.pause_work_session(user_id)
    await message.reply("Work session paused.")

@dp.message_handler(commands=['resume'])
async def resume_work(message: types.Message):
    user_id = message.from_user.id
    db.resume_work_session(user_id)
    await message.reply("Work session resumed.")

@dp.message_handler(commands=['users'])
async def list_users(message: types.Message):
    users = db.get_users()
    response = '\n'.join([f'{user[1]} (Chat ID: {user[2]})' for user in users])
    await message.reply(f"Users in the database:\n{response}")

if __name__ == '__main__':
    db.init_db()
    executor.start_polling(dp, skip_updates=True)
