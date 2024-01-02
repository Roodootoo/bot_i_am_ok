import asyncio
import logging
import sys
import requests
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from get_docker_secret import get_docker_secret

from data import save_new_user, add_to_list, get_users_list, del_from_list

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = get_docker_secret('token_tg', default="")
if not BOT_TOKEN:
    try:
        with open("token_tg", 'r') as token_tg:
            BOT_TOKEN = token_tg.read().rstrip('\n')
    except IOError as e:
        logger.critical("Одна или несколько обязательных переменных окружения не установлены!")
        sys.exit(1)

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

kb = [[
        KeyboardButton(text="Я - ОК"),
        KeyboardButton(text="ХЕЛП"),
        KeyboardButton(text="Просмотреть список")
    ]]
keyboard = ReplyKeyboardMarkup(keyboard=kb)


@dp.message(CommandStart())
async def send_welcome(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    save_new_user(user_id, user_name)
    await message.reply("Привет!\nЯ помогу не потеряться для друзей", reply_markup=keyboard)


@dp.message()
async def process_message(message: Message):
    user_id = message.from_user.id
    if message.text == 'Я - ОК' or message.text == 'ХЕЛП':
        users_list = get_users_list(user_id)
        try:
            for user in users_list:
                new_message = f"{user.username}: {message.text}"
                # url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={user.id}&text={new_message}"
                # print(requests.get(url).json())
                await bot.send_message(chat_id=user.id, text=new_message, reply_markup=keyboard)
        except:
            pass

    elif message.text == 'Просмотреть список':
        users_list = "\n".join(get_users_list(user_id))
        await message.reply(users_list)
        await message.reply("Чтобы добавить, напишите @username друга\nЧтобы удалить напишите -@username")

    elif message.text.find("@") == 0:
        chat_username = await bot.get_me()
        result = f'{add_to_list(user_id, message.text)} @{chat_username.username}'
        await message.reply(result)

    elif message.text.find("-@") == 0:
        chat_username = await bot.get_me()
        result = f'{del_from_list(user_id, message.text)} @{chat_username.username}'
        await message.reply(result)

    else:
        await message.reply("Не понимаю...", reply_markup=keyboard)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
