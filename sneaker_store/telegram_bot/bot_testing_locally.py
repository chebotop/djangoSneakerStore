import os
import logging
from typing import Any
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



logging.basicConfig(level=logging.INFO)
load_dotenv()

creds = ServiceAccountCredentials.from_json_keyfile_name('telegram_bot/data/secret_key.json')
scopes = [os.getenv('SCOPE_SHEETS'), os.getenv('SCOPE_DRIVE')]
gc = gspread.authorize(creds)


class Data:
    pending_update = []
    def __init__(self, gc):
        self.gc = gc
        self.sheet = gc.open('Cars and tip').sheet1
        self.data = self.sheet
        # Переделаю. Будет только self.sheet. Если команда update - цикл по списку из данных. Список составляется в глобальную переменную и должен не допускать дублирования

    def get(self):
        return self.data.get_all_values()

    def add_new_data(self, new_data):
        if new_data == list and len(new_data) == 3 or new_data == str and len(new_data.split()):
            self.pending_update.append(new_data)
        elif new_data == str and len(new_data.split(' ')) == 3:
            self.pending_update.append(new_data.split())

    def update_data(self):
        self.sheet.append_rows(self.pending_update)
        

data = Data(gc) # Создаем объект класса Data для работы с таблицей


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
            return ' '.join(sublist) # Возвращает строку!
    else:
        return False


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_args(message: types.Message, state: FSMContext):
    if message.text == 'update':
        data.update_data()
    if len(message.text.split('\n') > 1):
        lines = message.text.split('\n')
        logging.info(f"Получены аргументы: {lines}")
        added_count = 0
        for line in lines:
            args = line.split()
            number = args[0]
            # проверка выдаст ли return_existing_data(number).split() данные в формате ['номер','модель','бонус']
            logging.info(return_existing_data(number).split())
            if len(args) == 3 and not is_number_exist(number):
                logging.info(f"Number: {number}")
                data.add_new_data(args)
                added_count += 1
            # Проверка, вдруг я добавляю запись про машину, которая уже была, но клиент оставил другую сумму чаевых 
            elif len(args) == 3 and is_number_exist(number) and args[2] != return_existing_data(number).split()[2]:
                        data.add_new_data(args)
        if added_count:
            await message.answer(f"Добавлено {added_count} записей.")
        else:
            await message.answer(f"Нет данных")


def run_bot():
    from aiogram import executor
    executor.start_polling(dp)