import os
import dotenv
import aiogram.utils.markdown as md

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

import database
import models


# Loading environment variables into the project
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

API_TOKEN = os.environ.get('BOT_TOKEN')
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class UserForm(StatesGroup):
    login = State()
    age = State()
    gender = State()
    password = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    await UserForm.login.set()
    await message.reply("Hi there! What's your login?")


@dp.message_handler(state=UserForm.login)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user login
    """
    async with state.proxy() as data:
        data['login'] = message.text
    await UserForm.next()
    await message.reply("How old are you?")


@dp.message_handler(lambda message: not message.text.isdigit(), state=UserForm.age)
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    """
    Process user age
    """
    await UserForm.next()
    await state.update_data(age=int(message.text))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")
    await message.reply("What is your gender?", reply_markup=markup)


@dp.message_handler(state=UserForm.gender)
async def process_gender(message: types.Message, state: FSMContext):
    """
    Process user gender
    """
    async with state.proxy() as data:
        data['gender'] = message.text
        markup = types.ReplyKeyboardRemove()
    await UserForm.next()
    await message.reply("Can you write password&", reply_markup=markup)


@dp.message_handler(state=UserForm.password)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user password and create user account in db
    """
    async with state.proxy() as data:
        data['password'] = message.text
        new_user = models.User(
            login=md.bold(data['login']).replace('*', ''),
            first_name=message.from_user.first_name,
            age=md.bold(data['age']).replace('*', ''),
            gender=md.bold(data['gender']).replace('*', ''),
            password=generate_password_hash(
                md.bold(data['password']).replace('*', ''),
                method='sha256'
            ),
            telegram_id=message.from_user.id,
            telegram_username=message.from_user.username
           )
        try:
            database.db_session.add(new_user)
            database.db_session.commit()
        except IntegrityError:
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text('You already create account!'),
                    sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        except Exception:
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text('We were unable to create a user with this data...'),
                    sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text('Hi! Nice to meet you,', message.from_user.first_name),
                    md.text('Age:', md.code(data['age'])),
                    md.text('Gender:', data['gender']),
                    md.text('User with login', md.bold(data['login']), 'was created'),
                    sep='\n',
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
