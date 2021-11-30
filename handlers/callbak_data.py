import asyncio
import json
from pyrogram import errors
from aiogram import types
from misc import dp, bot
from .sqlit import change_status,cheak_black
import random


from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

text_time = """<b>⚠️Внимание⚠️</b>

Посмотри видео от начала до конца и сделай всё как в нём говорится!

После нажимай - Я выполнил(а)✅ / Я понял(а)✅"""

photo1 = 'AgACAgIAAxkBAAMlYZnkbxzeWQ2X-BPxA0rONFXicoAAAsm1MRvusZFIOZEYAxlhvskBAAMCAANzAAMiBA' #Опрос
photo2 = 'AgACAgIAAxkBAAMmYZnkotmfz-_gl8CuiNKsk1IZzu4AAua1MRvusZFIc8WNea3MjGQBAAMCAANzAAMiBA' #Начнем с создания телегерам канала😎
photo3 = 'AgACAgIAAxkBAAMnYZnk302u9mcS-IoP9VSRcxFx7qAAAva1MRvusZFIxWyT54RxTD8BAAMCAANzAAMiBA' #Обновляем канал в телеграмме
photo4 = 'AgACAgIAAxkBAAMoYZnk_gABMrKzgrpKsFYR-CAZcPsiAAIBtjEb7rGRSDIXxutx2InYAQADAgADcwADIgQ' #Телеметр
photo5 = 'AgACAgIAAxkBAAMpYZnlKHvsNx1BQLkjChN7C9e83XkAAgq2MRvusZFIsNCsQxaHROUBAAMCAANzAAMiBA' #Создаём бота для публикации постов в телеграм канал
photo6 = 'AgACAgIAAxkBAAMqYZnlVZbJWuXwb0_JifFEM0nWULoAAju2MRvusZFIH6Nu37WOAgIBAAMCAANzAAMiBA' #Подключаем бота для монетизации просмотров
photo7 = 'AgACAgIAAxkBAAMrYZnlhrDAGRztau3gpD_hkKwohpQAAoO3MRvusZlI90stPgtVJQQBAAMCAANzAAMiBA' #Промежуточные результаты!
photo8 = 'AgACAgIAAxkBAAMsYZnloPq7r_6QDp-e5v7czwtT0hwAAnS3MRvsfqhI9HbfWQ3LxScBAAMCAANzAAMiBA' #Наполняем контентом (фильмами) телеграм канал с фильмами
photo9 = 'AgACAgIAAxkBAAMtYZnlwwUZc8l1a9aCr0s8OcujSkoAAoK3MRvsfqhIjVX7Cg5FEloBAAMCAANzAAMiBA' #Информация о монетизации трафика
photo10 = 'AgACAgIAAxkBAAMuYZnl40RW0Z4Po4kE3RqGBYDvBZEAAg-0MRvsfrBIsB9_zPAzRxcBAAMCAANzAAMiBA' #Создаем "ПРОКЛАДКУ"
photo11 = 'AgACAgIAAxkBAAMvYZnmAwZv1dBmIyUZmyX9eEtYdrkAAiG0MRvsfrBINLOwX3tXuNABAAMCAANzAAMiBA' #Создание киви кошелька и получение статуса "Основной"
photo12 = 'AgACAgIAAxkBAAMwYZnmJvp2QgAB0z-OOZ6ap4CMy3OaAAIQtDEb7H6wSKlWQpAVXjALAQADAgADcwADIgQ' #Регистрация в боте прокладки, для монетизации трафика и проверки счетчика бота!
photo13 = 'AgACAgIAAxkBAAMxYZnmT2zxwELUV4E14g2FVJfnMdkAAhG0MRvsfrBIb3wiLju-cZwBAAMCAANzAAMiBA' #Добываем контент с YouTube
photo14 = 'AgACAgIAAxkBAAMyYZnmbIC48NyGYOpb5VVWjMMHQHsAAkO0MRvsfrBIL-o2O1aPc5wBAAMCAANzAAMiBA' #Готовим контент (фрагменты видео) для Тик Ток
photo15 = 'AgACAgIAAxkBAAMzYZnmj_HHdzvxcJhnHsAO_fCoXpQAAmy0MRvsfrBIUJ0BBKTubjcBAAMCAANzAAMiBA' #Учимся подбирать хештеги и делаем заготовку к видео!
photo16 = 'AgACAgIAAxkBAAM0YZnmtX3nE45vD6RB8WuLX3BaLOgAAie1MRuoWbBIyHR8MpGtt2YBAAMCAANzAAMiBA' #Устанавливаем и учимся пользоваться клинером!
photo17 = 'AgACAgIAAxkBAAM1YZnm3Ar5O2ZR9qUV8muhJmT3gBEAAh62MRuoWbBIzR7aA7XaVIMBAAMCAANzAAMiBA' #Заливаем нарезки в TikTok!
photo18 = 'AgACAgIAAxkBAAM2YZnm_Fxmu6hp-DznNj7rHTMY3AQAAiC2MRuoWbBIceFgrVFGxNUBAAMCAANzAAMiBA' #Информация по таймингам!
photo19 = 'AgACAgIAAxkBAAM3YZnnNa0FOTOCiDZus1RpgH7wJJAAAoi0MRuoWbhIozrRzBswW4ABAAMCAANzAAMiBA' #Финиш

video2 = 'BAACAgIAAxkBAAIFLWGmRplVbltHshDdYhDKyCzf9I0fAAJMEgACLTkoSehLiHxY7lKvIgQ'
video3 = 'BAACAgIAAxkBAAIFLmGmSNvaXqB14ddFJ9BA7yj-bAPSAAL0EgACLTkoSdLuCOJzvlPGIgQ'

class reg_p(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()

akk1 = 0
akk2 = 0
akk3 = 0
akk4 = 0
akk5 = 0
akk6 = 0
akk7 = 0
akk8 = 0
akk9 = 0
akk10 = 0
akk11 = 0
akk12 = 0
akk13 = 0
akk14 = 0
akk15 = 0
akk16 = 0
akk17 = 0
akk18 = 0

num = random.randint(2,18)

ignor_list = [0]
async def akkaut1(): #+79867995615
    from pyrogram import Client,idle,handlers
    app1 = Client('session1', 15429738, 'c147b713a6e1e7cbcdc0f92565605945')
    await app1.start()
    return app1

async def akkaut2(): #79867996353
    from pyrogram import Client,idle,handlers
    app2 = Client('session2', 17863610, '29204188291a4e719ffcb2f47a64465c')
    await app2.start()
    return app2
async def akkaut3(): #+79867996106
    from pyrogram import Client,idle,handlers
    app3 = Client('session3', 10519431, '34d9304c43433e76c035adaa8d68bfea')
    await app3.start()
    return app3

async def akkaut4(): #+79228216535
    from pyrogram import Client,idle,handlers
    app4 = Client('session4', 13164973, 'eb273111bceeb88b4a86804de21ebf68')
    await app4.start()
    return app4

async def akkaut5(): #+79228215677
    from pyrogram import Client,idle,handlers
    app5 = Client('session5', 19033993, 'b0113f5c4c807f47a39583e1c940c2e9')
    await app5.start()
    return app5

async def akkaut6(): #+79228215833
    from pyrogram import Client,idle,handlers
    app6 = Client('session6', 15324017, 'cab7928a596f34a201f229070abe252f')
    await app6.start()
    return app6

async def akkaut7(): #+79228215700
    from pyrogram import Client,idle,handlers
    app7 = Client('session7', 19770891, '298e60af1f84fba0a79868dcc3d6d542')
    await app7.start()
    return app7

async def akkaut8(): #+79325445644
    from pyrogram import Client,idle,handlers
    app8 = Client('session8', 17214899, 'a1129178e89e49eaaa2c99ae0f11debf')
    await app8.start()
    return app8

async def akkaut9(): #+79325443960
    from pyrogram import Client,idle,handlers
    app9 = Client('session9', 11971822, '657ee3f2eb59eff0d0095324c5d1bb34')
    await app9.start()
    return app9

async def akkaut10(): #+79328610075
    from pyrogram import Client,idle,handlers
    app10 = Client('session10', 15030107, '128417e785ff07dee773827f01e5e319')
    await app10.start()
    return app10

async def akkaut11(): #+79328529294
    from pyrogram import Client,idle,handlers
    app11 = Client('session11', 10053853, 'fd4a45d627e940a11d8d1b6077833ccf')
    await app11.start()
    return app11

async def akkaut12(): #+79328650388
    from pyrogram import Client,idle,handlers
    app12 = Client('session12', 16900797, 'a801fa6c8169859d99989dc100fddbfe')
    await app12.start()
    return app12

async def akkaut13(): #+79228215920
    from pyrogram import Client,idle,handlers
    app13 = Client('session13', 11364559, '7ea5620e981d93ba766d89df316e9e32')
    await app13.start()
    return app13

async def akkaut14(): #+79328622646
    from pyrogram import Client,idle,handlers
    app14 = Client('session14', 14369126, 'f2ba7b20cde3f0313ed3d6abd0c28160')
    await app14.start()
    return app14

async def akkaut15(): # +79228215770
    from pyrogram import Client,idle,handlers
    app15 = Client('session15', 18188269, 'd6d8c42f800e2f45ca3b297f8ef6d83b')
    await app15.start()
    return app15

async def akkaut16(): # +79228216313
    from pyrogram import Client,idle,handlers
    app16 = Client('session16', 13014654, '6086819e51966f88a27357fd07a41391')
    await app16.start()
    return app16

async def akkaut17(): # +79228215898
    from pyrogram import Client,idle,handlers
    app17 = Client('session17', 11149116, 'c60979a4c2c6e82d1fabdb981e941085')
    await app17.start()
    return app17

async def akkaut18(): # +79228215828
    from pyrogram import Client,idle,handlers
    app18 = Client('session18', 12663241, '46c99cb112f8c8942bc6b3e3eb9ce0d1')
    await app18.start()
    return app18


async def akkaunts(n,name,id):
    if int(cheak_black(id)) == 0:
        global akk1,akk2,akk3,akk4,akk5,akk6,akk7,akk8,akk9,akk10,akk11,akk12,akk13,akk14,akk15,akk16,akk17,akk18
        if akk1 == 0:
            akk1 = await akkaut1()
        if akk2 == 0:
            akk2 = await akkaut2()
        if akk3 == 0:
            akk3 = await akkaut3()
        if akk4 == 0:
            akk4 = await akkaut4()
        if akk5 == 0:
            akk5 = await akkaut5()
        if akk6 == 0:
            akk6 = await akkaut6()
        if akk7 == 0:
            akk7 = await akkaut7()
        if akk8 == 0:
            akk8 = await akkaut8()
        if akk9 == 0:
            akk9 = await akkaut9()
        if akk10 == 0:
            akk10 = await akkaut10()
        if akk11 == 0:
            akk11 = await akkaut11()
        if akk12 == 0:
            akk12 = await akkaut12()
        if akk13 == 0:
            akk13 = await akkaut13()
        if akk14 == 0:
            akk14 = await akkaut14()
        if akk15 == 0:
            akk15 = await akkaut15()
        if akk16 == 0:
            akk16 = await akkaut16()
        if akk17 == 0:
            akk17 = await akkaut17()
        if akk18 == 0:
            akk18 = await akkaut18()


        akks = [0,akk1,akk2,akk3,akk4,akk5,akk6,akk7,akk8,akk9,akk10,akk11,akk12,akk13,akk14,akk15,akk16,akk17,akk18] #Нулевой эллемент - Ноль


        a = await akks[n].create_channel(title='ОБНОВИ ЭТО НАЗВАНИЕ')
        await akks[n].send_message(chat_id=a.id, text=f"""<b>Фильмы 2021 скрыты от посторонних глаз. И доступны на приватном канале по ссылке ниже. Заходи и следуй инструкции</b>
    
<a href = https://t.me/MovieAndSerialsBot?start={name}>🍿НАЧАТЬ СМОТРЕТЬ🍿</a>""", disable_web_page_preview=True)

        try:
            await akks[n].add_chat_members(chat_id=a.id, user_ids = id)
        except errors.PeerIdInvalid:
            await akks[n].delete_channel(chat_id=a.id)
            return 8931
        except errors.UserPrivacyRestricted:
            await akks[n].delete_channel(chat_id=a.id)
            return 8932
        except:
            return 8933


        await akks[n].add_chat_members(chat_id=a.id, user_ids=id)

        await akks[n].promote_chat_member(chat_id=a.id, user_id=id, can_manage_chat=True, can_change_info=True,can_post_messages=True, can_edit_messages=True, can_delete_messages=True,can_restrict_members=True, can_invite_users=True, can_pin_messages=True,can_manage_voice_chats=True)
        url = await akks[n].export_chat_invite_link(chat_id=a.id)
        return url



@dp.callback_query_handler(text = 'reg_prokladka', state = "*")
async def reg_prokladka(call, state: FSMContext):
    if int(cheak_black(call.message.chat.id)) == 0:
        try:  # ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
            time11 = (await state.get_data())['time11']
        except:  # ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
            await reg_p.step1.set()
            time11 = 1

        if time11 == 1:
            await reg_p.step2.set() #ОЖИДАЕМ НАЗВАНИЕ КАНАЛА ЧЕРЕЗ @
            await call.message.answer("""<b>Отправь ссылку на свой канал через @ (собачку), как показано на видео!</b>
    
Не знаешь как это сделать? Посмотри видео еще раз😉""")

        else:
            await call.message.answer(text=text_time)

        await bot.answer_callback_query(call.id)  # Отвечаем на callback


@dp.message_handler(state=reg_p.step2, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    if int(cheak_black(message.chat.id)) == 0:
        if message.text[0] == '@':
            global ignor_list
            f = 0#КОЛИЧЕСТВО ПОПЫТОК КОНКРЕТНОГО ЧЕЛОВЕКА
            for i in ignor_list:
                if int(i) == int(message.chat.id):
                    f += 1

            if f < 5:
                ignor_list.append(message.chat.id)
                global num
                if num != 18:
                    num += 1
                else:
                    num = 1
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='Продолжить обучение ✅',callback_data='battun11')
                markup.add(bat_a)

                # 8931 - Этот код ошибки означает что сессия не нашла человека
                # 8932 - У человека приватность
                # 8933 - С аккаунтом что-то не так. Нужно повторить попытку

                answer = await akkaunts(num,name=message.text,id= message.chat.id)
                try:
                    i = int(answer)
                    if i == 8931:
                        await message.answer(text="""Не могу создать тебе прокладку и добавить тебя туда.
        
Что бы это исправить переходи в свой чат команды и <b>напиши туда любое сообщение</b>

После этого повтори попытку""")
                    if i == 8932:
                        await message.answer(text="""Не могу создать тебе прокладку и добавить тебя туда.
        
Что бы это исправить переходи в настройки, нажимай

    - Конфидециальность
    - Группы и каналы
И выбери <b>ВСЕ</b>

После этого повтори попытку""")
                    if i == 8933:
                        num+=1
                        answer = await akkaunts(num, name=message.text, id=message.chat.id)
                        try:
                            i = int(answer)
                            if i == 8931:
                                await message.answer(text='Напишите сообщение в чат и повторите попытку')
                            if i == 8932:
                                await message.answer(text="""Не могу создать тебе прокладку и добавить тебя туда.
        
Что бы это исправить переходи в настройки, нажимай

    - Конфидециальность
    - Группы и каналы
И выбери <b>ВСЕ</b>

После этого повтори попытку""")
                            if i == 8933:
                                num += 1
                                answer = await akkaunts(num, name=message.text, id=message.chat.id)
                                try:
                                    i = int(answer)
                                    if i == 8931:
                                        await message.answer(text='Напишите сообщение в чат и повторите попытку')
                                    if i == 8932:
                                        await message.answer(text="""Не могу создать тебе прокладку и добавить тебя туда.
        
Что бы это исправить переходи в настройки, нажимай

    - Конфидециальность
    - Группы и каналы
И выбери <b>ВСЕ</b>

После этого повтори попытку""")
                                    if i == 8933:
                                        await message.answer(text='В боте произошла ошибка. Напиши снова имя своего канала через @')
                                except:  # Это значит что все хорошо
                                    await message.answerf(f"""Это прокладка👇
{answer}   

В дальнейшем используешь только эту ссылку📌

Ты админ в этом канале, тебе необходимо поменяй аву и имя канала -> как показано на видео!

Прокладка это твой дополнительный канал с ботом. Бот монетизирует трафик🤑 и соответственно защищает канал от прохождения ботов 🤖 в твой канал""", reply_markup=markup)
                                    await state.finish()

                        except:  # Это значит что все хорошо
                            await message.answer(f"""Это прокладка👇
{answer}   

В дальнейшем используешь только эту ссылку📌

Ты админ в этом канале, тебе необходимо поменяй аву и имя канала -> как показано на видео!

Прокладка это твой дополнительный канал с ботом. Бот монетизирует трафик🤑 и соответственно защищает канал от прохождения ботов 🤖 в твой канал""", reply_markup=markup)
                            await state.finish()

                except: #Это значит что все хорошо
                    await message.answer(f"""Это прокладка👇
{answer}   

В дальнейшем используешь только эту ссылку📌

Ты админ в этом канале, тебе необходимо поменяй аву и имя канала -> как показано на видео!

Прокладка это твой дополнительный канал с ботом. Бот монетизирует трафик🤑 и соответственно защищает канал от прохождения ботов 🤖 в твой канал""",reply_markup=markup)
                    await state.finish()


            else:
                await message.answer(text='Слишком много попыток. Повторите действие через 13 часов')
                await asyncio.sleep(46800) #46800
                for r in ignor_list: #УДАЛЯЕМ IDШНИК ИЗ IGNORE LIST
                    if int(r) == int(message.chat.id):
                        try:
                            ignor_list.remove(r)
                        except:
                            break




        else:
            await message.answer(text='Отправь название канала через @\n'
                                      'Пример : @kinoHD')


@dp.callback_query_handler(lambda call: True, state = '*')
async def answer_push_inline_button(call, state: FSMContext):
    if int(cheak_black(call.message.chat.id)) == 0:
        if call.data == 'bat_video2': #отправляем второе видео
            try:  # ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                bat_video2 = (await state.get_data())['bat_video2']
            except:  # ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                bat_video2 = 1

            if bat_video2 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='Я принимаю✅ правила спринта', callback_data='bat_video3')
                markup.add(bat_a)

                await bot.send_video(chat_id=call.message.chat.id,video=video2,caption="""❗️Важные правила спринта❗️""",reply_markup=markup)

                await state.update_data(bat_video3=0)
                await asyncio.sleep(60)  # 60 СЕК
                await state.update_data(bat_video3=1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'bat_video3': #отправляем второе видео
            try:  # ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                bat_video3 = (await state.get_data())['bat_video3']
            except:  # ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                bat_video3 = 1

            if bat_video3 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='Я всё посмотрел(а)', callback_data='battun1')
                markup.add(bat_a)

                await bot.send_video(chat_id=call.message.chat.id,video=video3,caption="""❗️Как пройти обучение, результативно❗️
    
❗️Как пользоваться ботом❗️""",reply_markup=markup)

                await state.update_data(time1 = 0)
                await asyncio.sleep(240)  # 4 минуты (240)
                await state.update_data(time1 = 1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun1':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time1 = (await state.get_data())['time1']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time1 = 1

            if time1 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='Пройти опрос', url= 'https://docs.google.com/forms/d/e/1FAIpQLSeGJHcayZRgyobipRz3UVaE0MIO6Ri8xGoZog9ipVpKaahJJg/viewform?usp=sf_link')
                bat_b = types.InlineKeyboardButton(text='Для чего нужен опрос', url= 'https://youtu.be/4OXF1dPaWMw')
                bat_c = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun2')
                markup.add(bat_a)
                markup.add(bat_b)
                markup.add(bat_c)
                await bot.send_photo(chat_id=call.message.chat.id,photo = photo1,reply_markup=markup)

                await state.update_data(time2=0)
                await asyncio.sleep(30)  #30 СЕК
                await state.update_data(time2=1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun2':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time2 = (await state.get_data())['time2']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time2 = 1

            if time2 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url = 'https://youtu.be/24Fx5ut4_zE')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun3')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id,photo = photo2,reply_markup=markup,caption="""<b>Начнем с создания телегерам канала😎</b>
        
Посмотри видео и создай свой телеграм канал🤩""")
                await state.update_data(time3=0)
                await asyncio.sleep(30)  # 30 СЕК
                await state.update_data(time3=1)


            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun3':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time3 = (await state.get_data())['time3']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time3 = 1

            if time3 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/9Y0NTrF9O-o')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun4')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo3, reply_markup=markup, caption="""Посмотри видео и приступай🤩""")

                await state.update_data(time4=0)
                await asyncio.sleep(30)  # 30 СЕК
                await state.update_data(time4=1)
            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun4':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time4 = (await state.get_data())['time4']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time4 = 1

            if time4 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/3royyFKNj_U')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun5')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo4, reply_markup=markup, caption="""<b>Подключаем аналитику телеграм каналов Telemetr</b>
    
🤖Ссылка на бот - @telemetrmebot

Смотри видео👇""")
                await state.update_data(time5 = 0)
                await asyncio.sleep(30)  # 30 СЕК
                await state.update_data(time5 = 1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun5':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time5 = (await state.get_data())['time5']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time5 = 1

            if time5 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/Vs-LbZ_IyE4')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun6')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo5, reply_markup=markup, caption="""<b>🤖Создаём бота для публикации постов в телеграм канал</b>
        
1️⃣Первый бот из видео - @BotFather
2️⃣Второй бот из видео - @ControllerBot
    
Смотри видео👇""")
                await state.update_data(time6=0)
                await asyncio.sleep(150)  # 150 СЕК
                await state.update_data(time6=1)


            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun6':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time6 = (await state.get_data())['time6']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time6 = 1

            if time6 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/cziZbu1uD70')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun7')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo6, reply_markup=markup, caption="""<b>🤖Подключаем бота для монетизации просмотров</b>
        
🤖Создаём бота для публикации постов в телеграм канал
    
1️⃣Первый бот из видео - @BotFather
2️⃣Второй бот из видео - @Film_Webmaster_bot
    
Смотри видео👇""")

                await state.update_data(time7=0)
                await asyncio.sleep(360)  # 360 СЕК
                await state.update_data(time7=1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun7':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time7 = (await state.get_data())['time7']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time7 = 1

            if time7 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/zDO96AuQhuc')
                bat_b = types.InlineKeyboardButton(text='Я понял(а)✅', callback_data='battun8')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo7, reply_markup=markup, caption="""<b>Промежуточные результаты!🤔</b>""")

                await state.update_data(time8=0)
                await asyncio.sleep(30)  # 30 СЕК
                await state.update_data(time8=1)
            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun8':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time8 = (await state.get_data())['time8']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time8 = 1

            if time8 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/jbMuArq-GTw')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun9')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo8, reply_markup=markup, caption="""<b>Наполняем контентом (фильмами) телеграм канал с фильмами🎬</b>""")
                await state.update_data(time9 = 0)
                await asyncio.sleep(330)  # (330)
                await state.update_data(time9 = 1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun9':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time9 = (await state.get_data())['time9']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time9 = 1

            if time9 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url = 'https://youtu.be/tqzYxQVQdGI')
                bat_b = types.InlineKeyboardButton(text='Я понял(а)✅', callback_data = 'battun10')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo9, reply_markup=markup, caption="""<b>Информация о монетизации трафика🤑</b>""")
                await state.update_data(time10=0)
                await asyncio.sleep(210)  # 210 СЕК
                await state.update_data(time10=1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun10':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time10 = (await state.get_data())['time10']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time10 = 1

            if time10 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url = 'https://youtu.be/BURMSRmrFCs') #ВИДЕО БУДЕТ ГОТОВО ПОСЛЕ СОЗАДНИЯ БОТА
                bat_b = types.InlineKeyboardButton(text='СОЗДАТЬ ПРОКЛАДКУ', callback_data = 'reg_prokladka')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo10, reply_markup=markup, caption="""<b>Создаем "ПРОКЛАДКУ"</b>
        
⚠️Будьте максимально внимательны при просмотре видео⚠️""")
                await state.update_data(time11=0)
                await asyncio.sleep(210)  #210 СЕК
                await state.update_data(time11=1)

            else:
                await call.message.answer(text=text_time)

        """ТУТ ЧЕЛОВЕК УЖЕ СОЗДАЛ СЕБЕ ПРОКЛАДКУ И НАЧИНАЕТ РЕГАТЬ КИВИ """

        if call.data == 'battun11':
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/QuHt-KxkVDg')
            bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun12')
            markup.add(bat_a)
            markup.add(bat_b)
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo11, reply_markup=markup, caption="""<b>Создание киви кошелька и получение статуса "Основной"</b>
    
<b>Берём ФИО</b> - https://randomus.ru/name 

<b>Берём паспортные данные</b> - https://www.reestr-zalogov.ru/search/index

<b>При запросе ИНН берём отсюда</b> - https://service.nalog.ru/inn.do



<b>⚠️Будьте максимально внимательны при просмотре видео⚠️</b>""")
            await reg_p.step1.set()
            await state.update_data(time12=0)
            await asyncio.sleep(210)  #210 СЕК
            await state.update_data(time12=1)

        if call.data == 'battun12':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time12 = (await state.get_data())['time12']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time12 = 1

            if time12 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/Sj2--iwqMbg')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun13')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo12, reply_markup=markup, caption="""<b>Регистрация в боте прокладки, для монетизации трафика и проверки счетчика бота!
        
Коротко о действиях:</b>
    
1️⃣ Переходите в бота 
2️⃣ Отправляете боту /reg
3️⃣ Отправляете боту ссылку на канал через @
4️⃣ Отправляете боту номер телефона на который зарегистрирован киви кошелек
5️⃣ Отправляете боту /stat для просмотра статистики трафика
    
    
<b>⚠️Будьте максимально внимательны при просмотре видео⚠️</b>""")
                await state.update_data(time13=0)
                await asyncio.sleep(120)  #120 СЕК
                await state.update_data(time13=1)


            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun13':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time13 = (await state.get_data())['time13']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time13 = 1

            if time13 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/qxgeLjKWMp8')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun14')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo13, reply_markup=markup, caption="""<b>Добываем контент с YouTube</b>
        
<b>Список You Tube каналов</b> - https://telegra.ph/YouTube-kanaly-s-trejlerami-11-18

<b>Телеграм боты для скачивания видео с YouTube 👇</b>
@SaveYoutubeBot
@Isave_You_Tube_bot
@YouTubaBot""")
                await state.update_data(time14=0)
                await asyncio.sleep(180)  # 180 СЕК
                await state.update_data(time14=1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun14':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time14 = (await state.get_data())['time14']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time14 = 1

            if time14 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/itidUKfx-W0')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun15')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo14, reply_markup=markup, caption="""<b>Готовим контент (фрагменты видео) для Тик Ток</b>""")
                await state.update_data(time15=0)
                await asyncio.sleep(240)  # 240 СЕК
                await state.update_data(time15=1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun15':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time15 = (await state.get_data())['time15']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time15 = 1

            if time15 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/W0KIxfsIdX8')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun16')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo15, reply_markup=markup, caption="""<b>Учимся подбирать хештеги и делаем заготовку к видео!</b>
        
        
<b>Шпаргалка по хэштегам</b>
Название (если много частей то указывать все части), жанр(ы), главные герои (если они знамениты), киностудия (#Марвел, #ДС и т.д), хэштеги по самому видео что там происходит (к примеру форсаж: #гонки, #машины, #крутыетачки и т.д) общие хэштеги (такие как #фильм #кино #сериал #мульт )""")
                await state.update_data(time16 = 0)
                await asyncio.sleep(150)  # 150 СЕК
                await state.update_data(time16 = 1)

            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun16':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time16 = (await state.get_data())['time16']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time16 = 1

            if time16 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/y9PblerUriA')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun17')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo16, reply_markup=markup, caption="""<b>Устанавливаем и учимся пользоваться клинером!</b>
        
Клинер для IPhone - https://apps.apple.com/ru/app/cleaner-clean-my-storage/id1499634651""")
                await state.update_data(time17=0)
                await asyncio.sleep(60)  # 60 СЕК
                await state.update_data(time17=1)
            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun17':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time17 = (await state.get_data())['time17']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time17 = 1

            if time17 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/e8Z6GAmMMQY')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun18')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo17, reply_markup=markup, caption="""<b>Заливаем нарезки в TikTok!</b>
        
<b>БОТ ВРЕМЕННЫХ ПОЧТ:</b> @TempMail_org_bot

<b>Не забывайте сохранять данные:</b>
- Пороль
- Никнейм канала
- Пороль

<b>⭕️Пороль рекомендую во всех аккаунтах ставить один и тот же, что бы потом не потерять и не забыть⭕️</b>""")
                await state.update_data(time18=0)
                await asyncio.sleep(750)  # 750 СЕК
                await state.update_data(time18=1)
            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun18':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time18 = (await state.get_data())['time18']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time18 = 1

            if time18 == 1:
                markup = types.InlineKeyboardMarkup()
                bat_a = types.InlineKeyboardButton(text='🍿ВИДЕО🍿', url='https://youtu.be/o-ce1Y_3i2A')
                bat_b = types.InlineKeyboardButton(text='Я выполнил(а)✅', callback_data='battun19')
                markup.add(bat_a)
                markup.add(bat_b)
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo18, reply_markup=markup, caption="""<b>Информация по таймингам!</b>""")
                await state.update_data(time19=0)
                await asyncio.sleep(90)  # 90 СЕК
                await state.update_data(time19=1)
            else:
                await call.message.answer(text=text_time)

        if call.data == 'battun19':
            try: #ПРОВЕРЯЕМ НЕ СЛЕТЕЛ ЛИ СЕТ
                time19 = (await state.get_data())['time19']
            except: #ЕСЛИ СЕТ СЛЕТЕЛ, ТО УСТАНАВЛИВАЕМ ЕГО ЗАНОВО И РАЗРЕШАЕМ ОТПРАВКУ ВИДОСА
                await reg_p.step1.set()
                time19 = 1

            if time19 == 1:
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo19, caption="""<b>Поздравляем с прохождением обучения🎉🎉🎉</b>
        
Не выключай уведомления у бота и не удаляй бот. Мы будем присылать важную информацию!""")
                change_status(call.message.chat.id)

            else:
                await call.message.answer(text=text_time)


        try:
            await bot.answer_callback_query(call.id)  # Отвечаем на callback
        except:
            pass