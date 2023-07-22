import sqlite3

from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text, CommandObject
from aiogram import Bot
from filters import AdminFilter, SubFilter
import asyncio
import aiosqlite
import sys
sys.path.append('..')
from databaseclass import UserDb, RefDb, token

bot = Bot(token=token)
router = Router()

class StandId(StatesGroup):
    usid = State()

@router.message(Command(commands=['start']))
async def greets(message: Message, command: CommandObject):
    photo = FSInputFile('bot/fable.jpg')
    user = UserDb(message)
    builder = InlineKeyboardBuilder()
    builder.button(text='ОТКРЫТЬ📂', callback_data='getgold')
    await bot.send_photo(message.chat.id, photo, caption=f'Привет\nЖми на кнопку чтобы открыть "Fable" case рямо в телеграме!', reply_markup=builder.as_markup())
    if_new = await user.add_user()
    try:
        # async with aiosqlite.connect("users.db", timeout=100) as db:
        #     await db.execute(f'insert into users ("id", "name", "surname", "lang", "date") values ("{message.chat.id}", "{message.from_user.first_name}", "{message.from_user.last_name}", "{message.from_user.language_code}", "{message.date}")')
        #     if (command.args):
        #         await db.execute(f'update ref set amount = amount + 1 where name = "{command.args}"')
        #     await db.commit()
        if command.args and if_new:
            await RefDb.increase(command.args)
    except sqlite3.IntegrityError as e:
        pass
    except Exception as e:
        print(e)

@router.callback_query(Text(text='getgold'))
async def getgold(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, 'ОТКРЫВАЕМ КЕЙС')
    await bot.send_chat_action(call.message.chat.id, 'typing')
    await asyncio.sleep(2.5)
    photo = FSInputFile('bot/knife.jpg')
    builder = InlineKeyboardBuilder()
    builder.button(text='ЗАЛУТАТЬ НА СВОЙ АККАУНТ✅', callback_data='getknife')
    await bot.send_photo(call.message.chat.id, photo, caption=f'<b><i>ЧТООООО😱😱</i></b>\n<u><b>ТЫ ВЫБИЛ БАБОЧКУ "BLACK WIDOW"</b></u>', reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(Text(text='getknife'), SubFilter())
async def getknife(call: CallbackQuery, state: FSMContext):
    await state.set_state(StandId.usid)
    await bot.send_message(call.message.chat.id, 'ВВЕДИ СВОЙ STANDOFF 2 ID')

@router.message(StandId.usid)
async def getid(message: Message, state: FSMContext):
    await state.clear()
    await bot.send_message(message.chat.id, f'ЗАЯВКА НА ВЫВОД НОЖА BUTTERFLY "BLACK WIDOW" НА АККАНУТ {message.text} ПОДАНА\nСЕЙЧАС ОПЕРАТОР ОТПИШЕТ И ДАСТ ПОДАЛЬШИЕ ИНСТРУКЦИИ')





