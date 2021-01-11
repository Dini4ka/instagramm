from instabot import BOTS
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


bot = Bot(token='1530895721:AAHwJVW512nOzpo1bb-piaqUr10SMiqqFYg')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# создаём форму и указываем поля
class Form(StatesGroup):
    link = State()
    text = State()
    time = State()
    count = State()

# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Начинаем наш диалог
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.link.set()
    await message.reply("Привет! Укажи ссылки на посты\nСсылки указывайте через пробле\n автор - @velord")



# Сюда приходит ответ с ссылкой
@dp.message_handler(state=Form.link)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['link'] = message.text

    await Form.next()
    await message.reply("Какой будет текст комментария ?\n Если ники - то укажите их через проебл")


# Принимаем текст и узнаём периодичность
@dp.message_handler(state=Form.text)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['text'] = message.text
    await Form.next()

    await message.reply("Укажи переодичность")


# Сохраняем пeреодичность, узнаём кол-во сообщений
@dp.message_handler(state=Form.time)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['time'] = message.text
    await Form.next()

    await message.reply("И было бы неплохо знать сколько сообщений надо отправить")


# Сохраняем кол-во сообщений и запускаем скрипт
@dp.message_handler(state=Form.count)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['count'] = message.text
    await Form.next()

    await message.answer("готово")
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('link:', data['link']),
            md.text('text:', data['text']),
            md.text('time:', data['time']),
            md.text('count:', data['count']),
            sep='\n',
        ),
    )

    await message.answer("Боты запущены, начинаю работу")
    letter = data['time'][len(data['time']) - 1]
    if letter != 's' and letter != 'h' and letter != 'd' and letter != 'm':
        await state.finish()
    links = data['link'].split(' ')
    nicks = data['text'].split(' ')
    try:
        BOTS.type_comments(links,nicks,data['time'],int(data['count']))
        await message.answer("Выполнено")
    except:
        await message.answer("Закрыты комментарии или скрытый профиль,\nтакже может быть вы неккоректно укзали время.\nПропишите  \start ,начните сначала  и будьте внимательны")
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
