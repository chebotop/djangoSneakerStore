import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
creds = ServiceAccountCredentials.from_json_keyfile_name('telegram_bot/data/secret_key.json')
scopes = [os.getenv('SCOPE_SHEETS'), os.getenv('SCOPE_DRIVE')]


def fetch_data_from_gsheets():
    return gspread.authorize(creds).open('Cars and tip').sheet1


def is_number_exist(text_input):
    data = fetch_data_from_gsheets().get_all_values()
    keyword = text_input.split()[0]  # Берем только первое слово из строки, так как это номер
    for sublist in data:
        if keyword.lower() in sublist[0].lower():
            return True
    return False


def return_existing_data(number):
    data = fetch_data_from_gsheets().get_all_values()
    keyword = number.split()[0]  # Берем только первое слово из строки, так как это номер
    for sublist in data:
        if keyword.lower() in sublist[0].lower():
            return ' '.join(sublist)


def add_new_data(data):
    fetch_data_from_gsheets().append_row(data)


TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    awaiting_args = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Введите номерной знак")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_args(message: types.Message, state: FSMContext):
    lines = message.text.split('\n')
    added_count = 0
    
    for line in lines:
        args = line.split()
        number = args[0]
        
        if len(args) == 3 and not is_number_exist(number):
            add_new_data(args)
            added_count += 1
        elif len(args) == 3 and is_number_exist(number):
            previous_data = return_existing_data(number)
            await message.answer(f"Запись с номером '{number}' уже существует и была проигнорирована.\nПрошлая запись: {previous_data}")
        else:
            await message.answer(f"Строка '{line}' не соответствует формату и была пропущена.")

    if added_count:
        await message.answer(f"Добавлено {added_count} записей.")
    else:
        await message.answer("Не было добавлено ни одной записи.")


def run_bot():
    from aiogram import executor
    executor.start_polling(dp)
