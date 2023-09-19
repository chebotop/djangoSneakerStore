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
    pending_update = []
    def __init__(self, gc):
        self.gc = gc
        self.sheet = gc.open('Cars and tip').sheet1
        self.data = self.sheet

    def get(self):
        return self.data.get_all_values()

    def add_new_data(self, new_data):
        if isinstance(new_data, list) and len(new_data) == 3 or isinstance(new_data, str) and len(new_data.split()):
            self.pending_update.append(new_data)
        elif isinstance(new_data, str) and len(new_data.split(' ')) == 3:
            self.pending_update.append(new_data.split())

    def update_data(self):
        logging.info(f"pending_update = {self.pending_update};\nself.sheet type = {type(self.sheet)}")
        self.sheet.append_rows(self.pending_update)
        

data = Data(gc) # Создаем объект класса Data для работы с таблицей


def is_number_exist(text_input):
    # Берет номер авто в виде строки или последовательность 'номер модель бонус' в виде списка строк, проверяет есть ли номер в базе.
    keyword = text_input
    object_data = data.get()
    if isinstance(text_input, str) or isinstance(text_input, str) and len(text_input.split() == 3): # Если получена строка, определяем первый элемент, который должен быть номером машины
        keyword = text_input.split()[0]  
    elif isinstance(text_input, list) and len(text_input) == 3:
        keyword = text_input[0]
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
    if message.text.lower() == 'update':
        data.update_data()
        await message.answer("Данные успешно обновлены.")
    elif len(message.text.split()) == 1 and is_number_exist(message.text) == True:
        answer = return_existing_data(message.text.split()[0])
        await message.answer(f"Найдена запись: {answer}")
        return True
    elif len(message.text.split()) == 3 or len(message.text.split('\n')) > 1:
        lines = message.text.split('\n')
        logging.info(f"Получены аргументы: {lines}")
        added_count = 0
    
        for line in lines:
            if line.strip():
                args = line.split()
                number = args[0]
                logging.info(type(number))
                existing_value = return_existing_data(number)
                existing_bool = is_number_exist(number)
                # проверка выдаст ли return_existing_data(number).split() данные в формате ['номер','модель','бонус']
                logging.info(f"Обработка: {existing_value}")
                if len(args) == 3 and not existing_bool:
                    logging.info(f"Number: {number}")
                    data.add_new_data(args)
                    added_count += 1
                # Проверка, вдруг я добавляю запись про машину, которая уже была, но клиент оставил другую сумму чаевых 
                elif len(args) == 3 and existing_bool:
                    if args[2] != existing_value.split()[2]:
                        await message.answer(f'Клиент на {existing_value.split()[1]} приезжал, дал другую сумму чаевых. Было {existing_value.split()[2]} шекелей')
                        data.add_new_data(args)
                    #Если машина есть, выдать ответ
                    elif args[2] == existing_value.split()[2]:
                        await message.answer(f'Клиент есть в базе и бонус такой же - {existing_value.split()[2]} шекелей')
        if added_count:
            await message.answer(f"Добавлено {added_count} записей.")

        

def run_bot():
    from aiogram import executor
    executor.start_polling(dp)
