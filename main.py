from aiogram import Bot, Dispatcher, types, F, html
from aiogram.filters import CommandStart, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from states import Code
import asyncio
import logging
from keyboards import menu_ru, menu_uz, skip, yes_or_no, choose_language, see_codes
from database import add_user_id, add_username, add_language, add_product, update_product_count, get_user_product_count, get_user_data, get_all_users, get_all_products
from aiogram.types import ReplyKeyboardRemove

dp = Dispatcher()

user_product = {'name': None, 'price': None, 'description': None, 'coder': None, 'photo': None}

@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer("Tilni Tanlang | Выберите язык", reply_markup=choose_language())

@dp.callback_query(F.data.in_(["uz", "ru"]))
async def language_section(call: types.CallbackQuery):
    if call.data == 'uz':
        await call.message.answer(f'Salom {html.bold(call.from_user.full_name)}!\nmen {html.link('CodeShop', "https://t.me/codeshop_uz")} Kanaliga elon berish uchun botman!', reply_markup=menu_uz())   
    elif call.data == 'ru':
        await call.message.answer(f'Привет {html.bold(call.from_user.full_name)}!\nя бот для реклама на канале {html.link('CodeShop', "https://t.me/codeshop_uz")} !', reply_markup=menu_ru())
    await call.message.delete()
    add_user_id(call.from_user.id)
    add_username(call.from_user.id, call.from_user.username)
    add_language(call.from_user.id, call.data)

@dp.message(and_f(F.text == "/statistika", F.chat.id == 7077167971))
async def see_users_answer(message: types.Message):
    await message.answer("Foydalanuvchilar soni: " + str(get_all_users()) + "\nKodlar soni: " + str(get_all_products()))

@dp.callback_query(F.data.in_(['sell_code', 'profile', 'see_codes']))
async def callback_query(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'sell_code':
        await call.message.answer('Kodingizni sotish uchun berilgan savollarga javob bering')
        await call.message.answer("Kodingiz nomini kiriting")
        await state.set_state(Code.name)
    elif call.data == 'profile':
        await call.message.answer(f" Foydalanuvchi: @{call.from_user.username}\n🆔 ID: {html.code(call.from_user.id)}\n🗒 Sotuvdagi mahsulotlar soni: {get_user_product_count(call.from_user.id)}", reply_markup=see_codes())
    elif call.data == 'see_codes':
        datas = get_user_data(call.from_user.id)
        if datas == None:
            await call.message.answer('Sotuvdagi kodlaringiz mavjud emas')
            return None
        await call.message.answer(f"Kodlaringiz 👇")
        for data in datas:
            if data['product_photo'] != "🛑 tashlab ketish":
                await call.message.answer_photo(photo=data['product_photo'], caption=f"🗒 Nomi: {html.bold(data['product_name'])} \n💸 Narxi: {html.bold(data['product_price'])} \n💬 Izohi: {html.bold(data['product_description'])}\n Texnologiyalar: {data['product_coder']}\n👤 Murojat uchun: @{call.from_user.username}")
            else:
                await call.message.answer(f"🗒 Nomi: {html.bold(data.get('product_name'))} \n💸 Narxi: {html.bold(data.get('product_price'))} \n💬 Izohi: {html.bold(data.get('product_description'))}\nRasmi: Yo'q\n Texnologiyalar: {data.get('product_coder')}\n👤 Murojat uchun: @{call.from_user.username}")
    await call.answer(cache_time=60)

@dp.message(Code.name)
async def code_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(name=message.text)
        await message.answer("Narxni kiriting (masalan: 7$ yoki 100 ming so'm)")
        await state.set_state(Code.price)
    else:
        await message.answer("Iltimos matn kiriting")
        await state.set_state(Code.name)

@dp.message(Code.price)
async def code_name(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Kodingiz uchun izoh kiriting")
    await state.set_state(Code.description)

@dp.message(Code.description)
async def code_name(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Kodingiz qaysi texnologiyagalarda yasalganini kiriting (masalan: Python, Django, HTML, CSS)")
    await state.set_state(Code.coder)

@dp.message(Code.coder)
async def get_coder(message: types.Message, state: FSMContext):
    await state.update_data(coder=message.text)
    await message.answer("Rasm bo'lsa yuboring yoki tashlab ketishni bosing", reply_markup=skip())
    await state.set_state(Code.photo)

@dp.message(Code.photo)
async def skip_this_step(message: types.Message, state: FSMContext):
    data = await state.get_data()
    technologies = ["#" + tech.replace(" ", "") for tech in data.get('coder').split(", ")]
    print(technologies)
    if message.content_type == 'photo':
        await state.update_data(photo=message.photo[-1].file_id)
        await message.answer_photo(photo=message.photo[-1].file_id, caption=f" Nomi: {data.get('name')} \n💸 Narxi: {data.get('price')} \n🗒 Izoh: {data.get('description')}\n🧑‍💻 Texnologiyalar: {data.get('coder')}\n👤 Murojat uchun: @{message.from_user.username}\n\n" + " ".join(technologies), reply_markup=yes_or_no())
    elif message.text == '🛑 tashlab ketish':
        await state.update_data(photo=message.text)
        await message.answer(f" Nomi: {data.get('name')} \n💸 Narxi: {data.get('price')} \n🗒 Izoh: {data.get('description')}\n🧑‍💻 Texnologiyalar: {data.get('coder')}\n👤 Murojat uchun: @{message.from_user.username}\n\n" + "".join(technologies), reply_markup=yes_or_no())
    user_product['name'] = data.get('name')
    user_product['price'] = data.get('price')
    user_product['description'] = data.get('description')
    user_product['photo'] = message.photo[-1].file_id if message.photo else message.text
    user_product['coder'] = data.get('coder')
    await state.clear()

@dp.message(F.text == '✅ Ha')
async def send_to_channel(message: types.Message, bot: Bot):
    data = user_product
    if data.get('photo') != '🛑 tashlab ketish':
        try:
            technologies = ["#" + tech.replace(" ", "") for tech in data.get('coder').split(", ")]
            await bot.send_photo(chat_id=-1002423260406, photo=data.get('photo'), caption=f" Nomi: {html.bold(data.get('name'))} \n💸 Narxi: {html.bold(data.get('price'))} \n🗒 Izohi: {html.bold(data.get('description'))}\n🧑‍💻 Texnologiyalar: {html.bold(data.get('coder'))}\n👤 Murojat uchun: @{message.from_user.username}\n\n" + " ".join(technologies))
        except:
            await bot.send_message(chat_id=-1002423260406, text=f" Nomi: {html.bold(data.get('name'))} \n💸 Narxi: {html.bold(data.get('price'))} \n🗒 Izohi: {html.bold(data.get('description'))}\n🧑‍💻 Texnologiyalar: {html.bold(data.get('coder'))}\n👤 Murojat uchun: @{message.from_user.username}\n\n" + " ".join(technologies))
    elif data.get('photo') == '🛑 tashlab ketish':
        await bot.send_message(chat_id=-1002423260406, text=f" Nomi: {html.bold(data.get('name'))} \n💸 Narxi: {html.bold(data.get('price'))} \n🗒 Izohi: {html.bold(data.get('description'))}\n🧑‍💻 Texnologiyalar: {html.bold(data.get('coder'))}\n👤 Murojat uchun: @{message.from_user.username}\n\n" + " ".join(technologies))
    add_product(message.from_user.id, data.get('name'), data.get('price'), data.get('description'), data.get('photo'), data.get('coder'))
    update_product_count(message.from_user.id)
    user_product.clear()
    await message.answer(f"Mahsilotingiz {html.link('Code Shop', 'https://t.me/codeshop_uz')} Kanaliga joyladi ✅\nProfile", reply_markup=menu_uz())

@dp.message(F.text == '❌ Yo\'q')
async def cancel(message: types.Message):
    user_product.clear()
    await message.answer('Bekor qilindi', reply_markup=ReplyKeyboardRemove())
    await message.answer("Profile", reply_markup=menu_uz())

async def main():
    bot = Bot(token='7436001942:AAGTZ6lszit73Y6LH58YMEXDo4t6H-oEpM4', default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))
    await bot.set_my_commands([types.BotCommand(command='start', description='Botni ishga tushirish')])
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
