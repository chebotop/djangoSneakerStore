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
gc = gspread.authorize(creds)


class Data:
    def __init__(self, gc):
        self.data = gc.open('Cars and tip').sheet1
    
    def update_data(self, gc):  
        self.data = gc.open('Cars and tip').sheet1

    def get(self):
        return self.data.get_all_values()
    
    def add_new_data(self, data):
        self.data.append_row(data)
    

data = Data(gc)



def is_number_exist(text_input):
    object_data = data.get()
    keyword = text_input.split()[0]  # Берем только первое слово из строки, так как это номер
    for sublist in object_data:
        if keyword.lower() in sublist[0].lower():
            return True
    return False


def return_existing_data(number):
    data_list = data.get()
    keyword = number.split(' ')[0]  # Берем только первое слово из строки, так как это номер
    logging.info(f"Ищем запись с номером: {keyword}")
    for sublist in data_list:
        if keyword.lower() in sublist[0].lower():
            logging.info(f"Найдена запись: {sublist}")
            return ' '.join(sublist)
    else:
        return False




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
    logging.info(f"Получены аргументы: {lines}")
    added_count = 0
    
    for line in lines:
        args = line.split()
        number = args[0]
        
        if len(args) == 3 and not is_number_exist(number):
            logging.info(f"Number: {number}, Respond: {is_number_exist(number)}")
            data.add_new_data(args)
            added_count += 1
        elif len(args) == 3 and is_number_exist(number):
            previous_data = return_existing_data(number)
            await message.answer(f"есть запись: {previous_data}")
    if added_count:
        await message.answer(f"Добавлено {added_count} записей.")
    else:
        number = message.text.split(' ')[0]
        if return_existing_data(number):
            await message.answer(f"Запись существует. Данные: {return_existing_data(number)}")
        else:
            await message.answer(f"По записи {number} нет данных")




def run_bot():
    from aiogram import executor
    executor.start_polling(dp)
