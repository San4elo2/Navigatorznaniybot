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

# ------------------- СОТРУДНИКИ ДЕКАНАТА -------------------
# === СОТРУДНИКИ ДЕКАНАТА (С ФОТО) ===
@router.message(F.text == "👨‍💼 Сотрудники деканата")
async def decanat(message: types.Message):
    # Просто замени ссылки на свои фото (загрузи на https://imgur.com)
    employees = [
        {
            "name": "Иванов Иван Иванович",
            "post": "Декан факультета",
            "cab": "Каб. 301",
            "phone": "+7 (3412) 77-60-10",
            "photo": "https://iimg.su/i/tVTzIK"   # ← твоё фото декана
        },
        {
            "name": "Петрова Анна Сергеевна",
            "post": "Зам. декана по учебной работе",
            "cab": "Каб. 302",
            "phone": "+7 (3412) 77-60-11",
            "photo": "https://iimg.su/i/tVTzIK"   # ← фото зама
        },
        {
            "name": "Сидорова Мария Петровна",
            "post": "Секретарь деканата",
            "cab": "Каб. 303",
            "phone": "+7 (3412) 77-60-12",
            "photo": "https://iimg.su/i/tVTzIK"   # ← фото секретаря
        },
        # ← можешь добавить ещё людей точно так же
    ]

    for emp in employees:
        caption = (
            f"<b>{emp['name']}</b>\n"
            f"{emp['post']}\n\n"
            f"Кабинет: {emp['cab']}\n"
            f"Телефон: {emp['phone']}"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
        ])

        await message.answer_photo(
            photo=emp["photo"],
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
        # Небольшая пауза между сообщениями, чтобы не было флуд-лимита
        await asyncio.sleep(0.5)
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















