import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
import asyncio
import logging

TOKEN = "8322577955:AAG8z3LcS2U77VGFYZb0LK8V7Xl71-YCX7s"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# Главное меню (клавиатура)
def get_main_menu():
    buttons = [
        [KeyboardButton(text="📅 Расписание")],
        [KeyboardButton(text="👨‍💼 Сотрудники деканата")],
        [KeyboardButton(text="👩‍🏫 Преподаватели")],
        [KeyboardButton(text="📚 Зачётная книжка")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# ------------------- КОМАНДА /start -------------------
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Я — <b>Навигатор Знаний</b> 📖\n"
        "Выбирай нужный раздел ниже 👇",
        reply_markup=get_main_menu()
    )

# ------------------- РАСПИСАНИЕ -------------------
@router.message(F.text.in_({"Расписание", "📅 Расписание"}))  # работает и с эмодзи, и без
async def schedule(message: types.Message):
    photo_url = "https://iimg.su/i/tVTzIK"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])

    caption = (
        "Расписание занятий\n\n"
    )

    await message.answer_photo(
        photo=photo_url,
        caption=caption,
        reply_markup=keyboard
    )

# === СОТРУДНИКИ ДЕКАНАТА — СПИСОК ФИО ===
@router.message(F.text == "👨‍💼 Сотрудники деканата")
async def decanat_list(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кузнецов Андрей Леонидович", callback_data="emp_1")],
        [InlineKeyboardButton(text="Мышкина Наталья Юрьевна", callback_data="emp_2")],
        [InlineKeyboardButton(text="Горохова Наталия Викторовна", callback_data="emp_3")],
        [InlineKeyboardButton(text="Вычужанина Елена Федоровна", callback_data="emp_4")],
        [InlineKeyboardButton(text="Клименко Екатерина Александровна", callback_data="emp_5")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])
    
    await message.answer(
        "<b>Сотрудники и преподаватели деканата</b>\n\nВыберите человека:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


# === ИНФОРМАЦИЯ О КОНКРЕТНОМ СОТРУДНИКЕ ===
@router.callback_query(F.data.startswith("emp_"))
async def show_employee(callback: types.CallbackQuery):
    employees = {
        "emp_1": {
            "name": "Кузнецов Андрей Леонидович",
            "post": "Декан",
            "phone": "8 (3412) 77-60-55",
            "email": "alkuznetsov_63@mail.ru",
            "vk": "-",
            "cab": "кафедра 6-203",
            "photo": "https://iimg.su/i/jkBVMz"
        },
        "emp_2": {
            "name": "Мышкина Наталья Юрьевна",
            "post": "Ведущий документовед",
            "phone": "8 (3412) 770971, 89199156319",
            "email": "managerzfo@yandex.ru",
            "vk": "https://vk.com/id61466470",
            "cab": "6-200",
            "subjects": "Получение справок, получение ведомостей посещаемости",
            "photo": "https://iimg.su/i/mj7VzN"
        },
        "emp_3": {
            "name": "Горохова Наталия Викторовна",
            "post": "Ведущий документовед",
            "phone": "8 (3412) 770971",
            "email": "human@istu.ru",
            "vk": "-",
            "cab": "6-200",
            "subjects": "Перевод",
            "photo": "https://iimg.su/i/hCfJJ6"
        },
        "emp_4": {
            "name": "Вычужанина Елена Федоровна",
            "post": "И.о Заведующего кафедры",
            "phone": "8-912-850-17-39",
            "email": "mim@istu.ru",
            "vk": "https://vk.com/id880437598",
            "cab": "6-501 или кафедра 6-509",
            "subjects": "Организационные вопросы, вопросы по учебе",
            "photo": "https://iimg.su/i/CJNQlJ"
        },
        "emp_5": {
            "name": "Клименко Екатерина Александровна",
            "post": "Ведущий документовед ",
            "phone": "8-912-016-47-71",
            "email": "e.a.trefilova@istu.ru",
            "vk": "https://vk.com/id880437598",
            "cab": "кафедра 6-509",
            "subjects": "Организационные вопросы, вопросы по учебе",
            "photo": "https://iimg.su/i/Xhp7A8"
        },
    }

    emp = employees.get(callback.data)
    if not emp:
        await callback.answer("Ошибка")
        return

    caption = (
        f"<b>{emp['name']}</b>\n"
        f"<i>{emp['post']}</i>\n\n"
        f"Телефон: {emp['phone']}\n"
        f"Почта: {emp['email']}\n"
        f"ВК: {emp['vk']}\n"
        f"Кабинеты: {emp['cab']}\n"
        f"Вопросы, по которым можно обратиться: {emp['subjects']}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать в ВК", url=emp['vk'])],
        [InlineKeyboardButton(text="← Назад к списку", callback_data="decanat_back")],
        [InlineKeyboardButton(text="Главное меню", callback_data="back_main")]
    ])

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=emp["photo"], caption=caption, parse_mode=ParseMode.HTML),
        reply_markup=keyboard
    )
    await callback.answer()


# === ВЕРНУТЬСЯ К СПИСКУ СОТРУДНИКОВ ===
@router.callback_query(F.data == "decanat_back")
async def decanat_back(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кузнецов Андрей Леонидович", callback_data="emp_1")],
        [InlineKeyboardButton(text="Мышкина Наталья Юрьевна", callback_data="emp_2")],
        [InlineKeyboardButton(text="Горохова Наталия Викторовна", callback_data="emp_3")],
        [InlineKeyboardButton(text="Вычужанина Елена Федоровна", callback_data="emp_4")],
        [InlineKeyboardButton(text="Клименко Екатерина Александровна", callback_data="emp_5")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])

    await callback.message.edit_text(
        "<b>Сотрудники и преподаватели деканата</b>\n\nВыберите человека:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await callback.answer()
# ------------------- ПРЕПОДАВАТЕЛИ -------------------
@router.message(F.text == "👩‍🏫 Преподаватели")
async def teachers(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кафедра ИТ", callback_data="dept_it")],
        [InlineKeyboardButton(text="Кафедра экономики", callback_data="dept_econ")],
        [InlineKeyboardButton(text="Кафедра иностранных языков", callback_data="dept_lang")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")],
    ])
    await message.answer("👩‍🏫 <b>Преподаватели</b>\n\nВыбери кафедру:", reply_markup=keyboard)

# ------------------- ЗАЧЁТНАЯ КНИЖКА -------------------
@router.message(F.text == "📚 Зачётная книжка")
async def zachetka(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть зачётку в браузере",
            url="https://lk.istu.ru/student/book"
        )],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")]
    ])
    await message.answer(
        "Электронная зачётная книжка ИжГТУ",
        reply_markup=keyboard
    )
# ------------------- ОБРАБОТКА CALLBACK -------------------
@router.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_main":
        await callback.message.edit_text(
            "Главное меню:",
            reply_markup=None
        )
        await callback.message.answer("Выбери раздел 👇", reply_markup=get_main_menu())
    
    # Примеры для расписаний и кафедр (можно расширять)
    elif callback.data.startswith("sched_"):
        await callback.message.edit_text("Тут будет расписание... (пока в разработке 🚧)")
    elif callback.data.startswith("dept_"):
        await callback.message.edit_text(f"Список преподавателей кафедры... (пока в разработке 🚧)")
    
    await callback.answer()

# Подключаем роутер
dp.include_router(router)

# ------------------- ЗАПУСК -------------------
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот Навигатор Знаний запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())


















