import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
creds = ServiceAccountCredentials.from_json_keyfile_name('telegram_bot/data/secret_key.json')
scopes=[os.getenv('SCOPE_SHEETS'), os.getenv('SCOPE_DRIVE')]


def fetch_data_from_gsheets():
    return gspread.authorize(creds).open('Cars and tip').sheet1


def is_number_exist(keyword):
    data = fetch_data_from_gsheets().get_all_values()
    # respond = [' '.join(sublist) for sublist in data if keyword.lower() in sublist[0].lower()]
    # return '\n'.join(respond) if respond else False
    for sublist in data:
        if keyword.lower() in sublist[0].lower():
            return True
    return False

def add_new_data(data):
    fetch_data_from_gsheets().append_row(data.split(' '))


# def choice_keyboard():
#     markup = InlineKeyboardMarkup()
#     item1 = InlineKeyboardButton("1. Сохранить ответ", callback_data="save_response")
#     item2 = InlineKeyboardButton("2. Продолжить", callback_data="continue")
#     markup.add(item1, item2)
#     return markup


TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    awaiting_additional_data = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Enter numberplate")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_message(message: types.Message, state: FSMContext):
    text = message.text

    if not is_number_exist(text):
        await message.answer("Введите группы из трех аргументов (номер, модель, бонус) через пробел:")
        await state.set_data({"awaiting_args": True})

@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_args_if_needed(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if data.get("awaiting_args", False):
        words = message.text.split()

        if len(words) % 3 == 0:
            for i in range(0, len(words), 3):
                args = words[i:i+3]
                add_new_data(args)
            await message.answer(f"Данные добавлены.")
            await state.reset_state()  # Сброс состояния
        else:
            await message.answer("Количество слов в сообщении должно быть кратно трем. Пожалуйста, проверьте ваш ввод.")



def run_bot():
    from aiogram import executor
    executor.start_polling(dp)