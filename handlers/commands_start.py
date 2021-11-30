from aiogram import types
from misc import dp,bot
from .sqlit import reg_user, info_members,cheak_black
from .callbak_data import reg_p
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

video_start = 'BAACAgIAAxkBAAIFLGGmRfSV_qvGGWQ4JjfHIrsNNSeiAAI_EgACLTkoSUtU1Cte8K4LIgQ'
reg_user(1)#Запуск в БД

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    if int(cheak_black(message.chat.id)) == 0:
        reg_user(message.chat.id)#Регистрация в БД
        await reg_p.step1.set()

        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Далее', callback_data='bat_video2')
        markup.add(bat_a)
        await bot.send_video(chat_id=message.chat.id,video=video_start,caption="""❗️Введение❗️""",reply_markup=markup)

        await state.update_data(bat_video2 = 0)
        await asyncio.sleep(60) #Длительность видоса каляна (60)
        await state.update_data(bat_video2 = 1)

