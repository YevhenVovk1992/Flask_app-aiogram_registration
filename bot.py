import os
import dotenv

from aiogram import Bot, Dispatcher, executor, types


# Loading environment variables into the project
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)


API_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Get news', callback_data='/get_news'))
    markup.add(types.InlineKeyboardButton('Go to web site', url='http://127.0.0.1:5000/'))
    await message.reply("Hello!", reply_markup=markup)


@dp.message_handler(commands=['add_user'])
async def get_news(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)