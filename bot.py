import logging, re
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from config import TOKEN,initial_connection
import pymysql

# connection to db
conn = initial_connection()

# initial bot
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# logging 
logging.basicConfig(level=logging.INFO)

# Class for storing bot states
class UserState(StatesGroup):
    WaitingForQuestion = State()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Зарегистрируйся используя /register ")

# Handler for user registration
@dp.message_handler(commands=['register'])
async def register_user(message: types.Message):
    # Extract user information from the message
    user_id = message.from_user.id
    #telegram_user_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    # Insert user data into the database
    insert_user(user_id, first_name, last_name, username)

    await message.reply("Вы успешно зарегистрированы!")

def insert_user(user_id, first_name, last_name, username):
    try:
        with conn.cursor() as cursor:
            # Execute the SQL query to insert the user data
            sql = "INSERT INTO users (id, first_name, last_name, username) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, first_name, last_name, username))
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка регистрации!{e}")

# Handler for user questions
@dp.message_handler()
async def handle_question(message: types.Message):
    user_id = message.from_user.id
    question = message.text

    # Reply to the user with an answer
    answer = get_answer(question)  
    
    # Save the question in the database
    save_chat(user_id, question, answer)

    await message.reply(answer)





# Save the question in the database
def save_chat(user_id, question, answer):
    try:
        with conn.cursor() as cursor:
            # Execute the SQL query to save the question
            sql = "INSERT INTO correspondence (user_id, question, answer) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, question, answer))
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка сохранения чата: {e}")


# Get the answer for a question 
def get_answer(question):
    res = None
    matches = re.findall(r'\d|[+-]', question)

    try:
        numbers = [int(match) for match in matches if match.isdigit()]
        operator = [match for match in matches if match in ['+', '-']][0]
    except Exception as e:
        res = "Неверная запись!"
        return res

    if operator == "+" and len(numbers) == 2:
        res = sum(numbers)
    elif operator == "-" and len(numbers) == 2:
        res = numbers[0] - numbers[1]
    else:
        res = 'Неверная запись!'

    return res



if __name__ == '__main__':
    executor.start_polling(dp)

