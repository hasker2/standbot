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
from aiogram.utils.deep_linking import create_start_link

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
            if (command.args.isdigit()):
                await UserDb.increase(int(command.args))
                await bot.send_message(command.args, "Кто-то перешел по ссылке!")
            else:
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
    refs = await UserDb.get_refs(call.message.chat.id)
    print(refs)
    if refs < 5:
        keyboard = [[KeyboardButton(text="Вывести нож🔥")]]
        kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        await bot.send_message(call.message.chat.id,
                               f"Твой нож готов!\nДля вывода пригласи всего лишь 5 человек по своей ссылке: {await create_start_link(bot, str(call.message.chat.id))}\nТы пригласил {refs}/5\nС помощью кнопки ниже ты сможешь смотреть количество людей, которых ты пригласил!",
                               reply_markup=kb)
        return
    await state.set_state(StandId.usid)
    await bot.send_message(call.message.chat.id, 'ВВЕДИ СВОЙ STANDOFF 2 ID')

@router.message(Text(text="Вывести нож🔥"))
async def refs(message: Message):
    refs = await UserDb.get_refs(message.chat.id)
    print(refs)
    if refs < 5:
        keyboard = [[KeyboardButton(text="Вывести нож🔥")]]
        kb = ReplyKeyboardMarkup(keyboard=keyboard)

        await bot.send_message(message.chat.id,
                               f"Твой нож готов!\nДля вывода пригласи всего лишь 5 человек по своей ссылке: {await create_start_link(bot, str(message.chat.id))}\nТы пригласил {refs}/5\nС помощью кнопки ниже ты сможешь смотреть количество людей, которых ты пригласил!",
                               reply_markup=kb)
    else:
        photo = FSInputFile('bot/knife.jpg')
        builder = InlineKeyboardBuilder()
        builder.button(text='ЗАЛУТАТЬ НА СВОЙ АККАУНТ✅', callback_data='getknife')
        await bot.send_photo(message.chat.id, photo,
                             caption=f'<b><i>ТВОЙ НОЖ УЖЕ ГОТОВ</i></b>\n<u><b>ЗАБЕРИ СВОЮ БАБОЧКУ "BLACK WIDOW"</b></u>',
                             reply_markup=builder.as_markup(), parse_mode="HTML")


@router.message(StandId.usid)
async def getid(message: Message, state: FSMContext):

    if message.text.isdigit():
        await bot.send_message(message.chat.id, f'ЗАЯВКА НА ВЫВОД НОЖА BUTTERFLY "BLACK WIDOW" НА АККАНУТ {message.text} ПОДАНА\nСЕЙЧАС ОПЕРАТОР ОТПИШЕТ И ДАСТ ПОДАЛЬШИЕ ИНСТРУКЦИИ')
        await state.clear()
    else:
        await bot.send_message(message.chat.id,
                               f'Введи правильный id❗')






