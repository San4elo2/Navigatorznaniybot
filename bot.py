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
        [InlineKeyboardButton(text="Шулакова Елена Витальевна", callback_data="emp_1")],
        [InlineKeyboardButton(text="Козлова Наталья Александровна", callback_data="emp_2")],
        [InlineKeyboardButton(text="Смирнов Дмитрий Сергеевич", callback_data="emp_3")],
        [InlineKeyboardButton(text="Волкова Ольга Николаевна", callback_data="emp_4")],
        [InlineKeyboardButton(text="Петров Алексей Владимирович", callback_data="emp_5")],
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
            "name": "Шулакова Елена Витальевна",
            "post": "Старший преподаватель",
            "phone": "—",
            "email": "evstud@gmail.com",
            "vk": "https://vk.com/id390204733",
            "cab": "кафедра 6-509, 6-501, 6-511",
            "subjects": "Введение в специальность, Теория менеджмента",
            "photo": "https://iimg.su/i/tVTzIK"   # ← замени на своё фото
        },
        "emp_2": {
            "name": "Козлова Наталья Александровна",
            "post": "Доцент, к.э.н.",
            "phone": "+7 (3412) 58-77-55 доб. 123",
            "email": "kozlova@istu.ru",
            "vk": "https://vk.com/id12345678",
            "cab": "6-507",
            "subjects": "Экономика предприятия, Управление персоналом",
            "photo": "https://iimg.su/i/tVTzIK"
        },
        "emp_3": {
            "name": "Смирнов Дмитрий Сергеевич",
            "post": "Старший преподаватель",
            "phone": "—",
            "email": "d.smirnov@istu.ru",
            "vk": "https://vk.com/dmitry_smirnov",
            "cab": "6-510",
            "subjects": "Информационные технологии в управлении, Базы данных",
            "photo": "https://iimg.su/i/tVTzIK"
        },
        "emp_4": {
            "name": "Волкова Ольга Николаевна",
            "post": "Заведующая кафедрой",
            "phone": "+7 (3412) 58-77-55 доб. 101",
            "email": "volkova.on@istu.ru",
            "vk": "https://vk.com/id9876543",
            "cab": "6-505",
            "subjects": "Стратегический менеджмент, Корпоративное управление",
            "photo": "https://iimg.su/i/tVTzIK"
        },
        "emp_5": {
            "name": "Петров Алексей Владимирович",
            "post": "Доцент, к.т.н.",
            "phone": "+7 (3412) 58-77-55 доб. 108",
            "email": "petrov.av@istu.ru",
            "vk": "https://vk.com/alex_petrov_istu",
            "cab": "6-508",
            "subjects": "Проектный менеджмент, Инновационный менеджмент",
            "photo": "https://iimg.su/i/tVTzIK"
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
        f"Дисциплины: {emp['subjects']}"
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
        [InlineKeyboardButton(text="Шулакова Елена Витальевна", callback_data="emp_1")],
        [InlineKeyboardButton(text="Козлова Наталья Александровна", callback_data="emp_2")],
        [InlineKeyboardButton(text="Смирнов Дмитрий Сергеевич", callback_data="emp_3")],
        [InlineKeyboardButton(text="Волкова Ольга Николаевна", callback_data="emp_4")],
        [InlineKeyboardButton(text="Петров Алексей Владимирович", callback_data="emp_5")],
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
















