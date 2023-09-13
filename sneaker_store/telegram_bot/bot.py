import os
import logging
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
    def __init__(self, gc):
        self.gc = gc
        self.sheet = gc.open('Cars and tip').sheet1
        self.data = self.sheet

    def update_data(self, new_row):
        self.data.append_row(new_row)

    def get(self):
        return self.data.get_all_values()

    def add_new_data(self, new_data):
        self.sheet.append_row(new_data)
        self.update_data(new_data)

    def update_gsheet(self):
        values = self.get()  # Retrieve data from local memory
        values_for_update = []

        for row in values:
            values_for_update.append(row)  # Add each row as a list

        range_ = f'A1:{chr(ord("A") + len(values[0]) - 1)}{len(values_for_update)}'

        body = {
            'values': values_for_update
        }
        result = self.sheet.update(range_, body)

        if result:
            print('Data updated successfully')
        else:
            print('Data update failed')


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


sent_responses = {}  # Словарь для отслеживания отправленных ответов

@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_args(message: types.Message, state: FSMContext):
    if message.text == 'update':
        data.update_gsheet()
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
        elif len(args) == 3 and is_number_exist(number) and number not in sent_responses:
            previous_data = return_existing_data(number)
            if previous_data[-1] != args[-1]:
                logging.info(f"prevdata: {previous_data}, args: {args}")
                data.add_new_data(args)
                await message.answer(f"машина приехала второй раз и бонус изменился, запись добавлена: \n{args}\nПредыдущие данные: {return_existing_data(number)}")
            sent_responses[number] = True
    
    if added_count:
        await message.answer(f"Добавлено {added_count} записей.")
    elif return_existing_data(message.text.split(' ')[0]) and number not in sent_responses:
        await message.answer(f"Запись существует. Данные: {return_existing_data(number)}")
        sent_responses[number] = True
    else:
        await message.answer(f"Нет данных")

def run_bot():
    from aiogram import executor
    executor.start_polling(dp)
