from aiogram import types
from misc import dp, bot
import sqlite3

import asyncio

from aiogram.dispatcher import FSMContext
from .sqlit import info_members,add_black,cheak_black
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 941730379 #Джейсон
ADMIN_ID_4 = 678623761 # Бекир


ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3,ADMIN_ID_4]

class reg1(StatesGroup):
    name1 = State()
    fname1 = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()

class black_dodik(StatesGroup):
    name1 = State()
    fname1 = State()

@dp.message_handler(commands=['admin'],state='*')
async def admin_ka(message: types.Message,state: FSMContext):
    await state.finish()
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_c = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_b = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_d = types.InlineKeyboardButton(text='Удаление ебланов', callback_data='black_user')

        markup.add(bat_a)
        markup.add(bat_c)
        markup.add(bat_b)
        markup.add(bat_d)

        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)


@dp.callback_query_handler(text='black_user')  #УДАЛЕНИЕ ДОДИКОВ
async def delite_dodik(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        markap = types.InlineKeyboardMarkup()
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        markap.add(bat0)
        await bot.send_message(text = 'Перешли сообщение от додика',chat_id=call.message.chat.id,reply_markup=markap)
        await black_dodik.name1.set()


@dp.message_handler(state=black_dodik.name1,content_types=['text','photo','video','video_note','voice']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    try:
        user_id = message.forward_from.id
        add_black(user_id)
        await message.answer('Пользователь удалён 🩸')

    except Exception as e:
        await message.answer('У пидора закрытый аккаунт')



@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def cheack_trafik(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = (info_members()) #КОЛИЧЕСТВО ВСЕХ ЧЕЛОВ
        await bot.send_message(call.message.chat.id, f'Количество пользователей: {a[0]}\n'
                                                     f'Финиширровало пользователей {a[1]}')

@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = open('server.db','rb')
        await bot.send_document(chat_id=call.message.chat.id, document=a)

########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note','voice']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr3 = message.text.split('\n')
    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    massiv_text = []
    massiv_url = []

    for but in arr3:
        new_but = but.split('-')
        massiv_text.append(new_but[0][:-1])
        massiv_url.append(new_but[1][1:])
        bat9 = types.InlineKeyboardButton(text=new_but[0][:-1],url=new_but[1][1:])
        murkap.add(bat9)



    try:
        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but = massiv_text ) # Обновление Сета
        await state.update_data(url_but = massiv_url)  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками
    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_massiv = data['text_but']
        url_massiv = data['url_but']
        for t in text_massiv:
            for u in url_massiv:
                bat = types.InlineKeyboardButton(text=t, url=u)
                murkap.add(bat)
                break

    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time WHERE finish_stat = '1'").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        if int(cheak_black(id)) == 0:
            await asyncio.sleep(0.03)
            try:
                await mess.copy_to(i[0],reply_markup=murkap)
                good += 1
            except:
                bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################