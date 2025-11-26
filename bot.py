import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
import asyncio
import logging

TOKEN = "8322577955:AAHsV4GOVDCsKdschVa1MzpJSWSGQ0zMewg"

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
        [KeyboardButton(text="Полезные кабинеты")],
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
        "<b>Сотрудники деканата</b>\n\nВыберите человека:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


# === ИНФОРМАЦИЯ О СОТРУДНИКЕ ===
@router.callback_query(F.data.startswith("emp_"))
async def show_employee(callback: types.CallbackQuery):
    employees = {
        "emp_1": {"name": "Кузнецов Андрей Леонидович", "post": "Декан", "phone": "8 (3412) 77-60-55", "email": "alkuznetsov_63@mail.ru", "vk": "—", "cab": "кафедра 6-203", "subjects": "Общие вопросы, утверждение документов", "photo": "https://iimg.su/i/CppwDT"},
        "emp_2": {"name": "Мышкина Наталья Юрьевна", "post": "Ведущий документовед", "phone": "8 (3412) 770971, 89199156319", "email": "managerzfo@yandex.ru", "vk": "https://vk.com/id61466470", "cab": "6-200", "subjects": "справки, получение ведомостей, переводы на другую специальность, сроки сессии, какие экзамены, сроки сессии. ", "photo": "https://iimg.su/i/nEbNmA"},
        "emp_3": {"name": "Горохова Наталия Викторовна", "post": "Ведущий документовед", "phone": "8 (3412) 770971", "email": "human@istu.ru", "vk": "—", "cab": "6-200", "subjects": "Перевод, восстановление, академы", "photo": "https://iimg.su/i/s1rWG0"},
        "emp_4": {"name": "Вычужанина Елена Федоровна", "post": "И.о. заведующего кафедрой", "phone": "8-912-850-17-39", "email": "mim@istu.ru", "vk": "https://vk.com/id880437598", "cab": "6-501 / 6-509", "subjects": "Организационные вопросы, учебный процесс", "photo": "https://iimg.su/i/U5YebV"},
        "emp_5": {"name": "Клименко Екатерина Александровна", "post": "Ведущий документовед", "phone": "8-912-016-47-71", "email": "e.a.trefilova@istu.ru", "vk": "https://vk.com/id880437598", "cab": "кафедра 6-509", "subjects": "Справки, заявления, зачётки", "photo": "https://iimg.su/i/Xhp7A8"},
    }

    emp = employees.get(callback.data)
    if not emp:
        await callback.answer("Ошибка", show_alert=True)
        return

    vk_url = emp["vk"] if emp["vk"].startswith("http") else None

    caption = (
        f"<b>{emp['name']}</b>\n"
        f"<i>{emp['post']}</i>\n\n"
        f"Телефон: {emp['phone']}\n"
        f"Почта: {emp['email']}\n"
        f"Кабинет: {emp['cab']}\n"
        f"По вопросам: {emp['subjects']}"
    )

    buttons = []
    if vk_url:
        buttons.append([InlineKeyboardButton(text="Написать в ВК", url=vk_url)])
    buttons += [
        [InlineKeyboardButton(text="Назад к списку", callback_data="decanat_back")],
        [InlineKeyboardButton(text="Главное меню", callback_data="back_main")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=emp["photo"], caption=caption, parse_mode=ParseMode.HTML),
        reply_markup=keyboard
    )
    await callback.answer()


# === ВЕРНУТЬСЯ К СПИСКУ — ИСПРАВЛЕННАЯ ВЕРСИЯ ===
@router.callback_query(F.data == "decanat_back")
async def decanat_back(callback: types.CallbackQuery):
    # Удаляем сообщение с фото и отправляем новое текстовое
    await callback.message.delete()  # удаляем старое фото

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кузнецов Андрей Леонидович", callback_data="emp_1")],
        [InlineKeyboardButton(text="Мышкина Наталья Юрьевна", callback_data="emp_2")],
        [InlineKeyboardButton(text="Горохова Наталия Викторовна", callback_data="emp_3")],
        [InlineKeyboardButton(text="Вычужанина Елена Федоровна", callback_data="emp_4")],
        [InlineKeyboardButton(text="Клименко Екатерина Александровна", callback_data="emp_5")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])

    await callback.message.answer(
        "<b>Сотрудники деканата</b>\n\nВыберите человека:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await callback.answer()

# === ПРЕПОДАВАТЕЛИ — СПИСОК ФИО ===
@router.message(F.text == "Преподаватели")
async def teachers_list(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Шулакова Елена Витальевна", callback_data="teacher_1")],
        [InlineKeyboardButton(text="Камалетдинов Денис Святославович", callback_data="teacher_2")],
        [InlineKeyboardButton(text="Груздева Татьяна Витальевна", callback_data="teacher_3")],
        [InlineKeyboardButton(text="Сальникова Кристина Владимировна", callback_data="teacher_4")],
        [InlineKeyboardButton(text="Шмелев Олег Валерьевич", callback_data="teacher_5")],
        # ←←← добавляй сюда новых преподавателей так же
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])
    
    await message.answer(
        "<b>Преподаватели кафедры</b>\n\nВыберите преподавателя:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


# === ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЕ ===
@router.callback_query(F.data.startswith("teacher_"))
async def show_teacher(callback: types.CallbackQuery):
    teachers = {
        "teacher_1": {
            "name": "Шулакова Елена Витальевна",
            "post": "Старший преподаватель",
            "phone": "—",
            "email": "evstud@gmail.com",
            "vk": "https://vk.com/id390204733",
            "cab": "6-509, 6-501, 6-511",
            "subjects": "Введение в специальность, Теория менеджмента",
            "photo": "https://iimg.su/i/jit4Kx"   # ← замени на своё
        },
        "teacher_2": {
            "name": "Камалетдинов Денис Святославович",
            "post": "Старший преподаватель",
            "phone": "-",
            "email": "Kamaletdinovden@mail.ru",
            "vk": "https://vk.com/id20529720",
            "cab": "6-501",
            "subjects": "Техника личного и коллективного здорово сбережения",
            "photo": "https://iimg.su/i/08xJwe"
        },
        "teacher_3": {
            "name": "Груздева Татьяна Витальевна",
            "post": "Преподаватель",
            "phone": "8-904-835-44-22",
            "email": "t.v.gruzdeva@gmail.com",
            "vk": "—",
            "cab": "6-501",
            "subjects": "Маркетинг",
            "photo": "https://iimg.su/i/no7OS8"
        },
        "teacher_4": {
            "name": "Сальникова Кристина Владимировна",
            "post": "Преподаватель",
            "phone": "8-951-192-44-04",
            "email": "kristina-zhelnova@yandex.ru",
            "vk": "-",
            "cab": "6-501",
            "subjects": "Эконометрика",
            "photo": "https://iimg.su/i/IzJIxN"
        },
        "teacher_5": {
            "name": "Шмелев Олег Валерьевич",
            "post": "Старший преподаватель",
            "phone": "-",
            "email": "oleshm+istu@gmail.com",
            "vk": "-",
            "cab": "6-509",
            "subjects": "Теория игр, Введение в информационные технологии",
            "photo": "https://iimg.su/i/4ejcG8"
        },
        # ←←← добавляй сюда новых преподавателей
    }

    t = teachers.get(callback.data)
    if not t:
        await callback.answer("Преподаватель не найден", show_alert=True)
        return

    vk_url = t["vk"] if t["vk"].startswith("http") else None

    caption = (
        f"<b>{t['name']}</b>\n"
        f"<i>{t['post']}</i>\n\n"
        f"Телефон: {t['phone']}\n"
        f"Почта: {t['email']}\n"
        f"Кабинет: {t['cab']}\n"
        f"Ведёт дисциплины:\n{t['subjects']}"
    )

    buttons = []
    if vk_url:
        buttons.append([InlineKeyboardButton(text="Написать в ВК", url=vk_url)])
    buttons += [
        [InlineKeyboardButton(text="Назад к списку", callback_data="teachers_back")],
        [InlineKeyboardButton(text="Главное меню", callback_data="back_main")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=t["photo"], caption=caption, parse_mode=ParseMode.HTML),
        reply_markup=keyboard
    )
    await callback.answer()


# === ВЕРНУТЬСЯ К СПИСКУ ПРЕПОДАВАТЕЛЕЙ ===
@router.callback_query(F.data == "teachers_back")
async def teachers_back(callback: types.CallbackQuery):
    await callback.message.delete()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Шулакова Елена Витальевна", callback_data="teacher_1")],
        [InlineKeyboardButton(text="Камалетдинов Денис Святославович", callback_data="teacher_2")],
        [InlineKeyboardButton(text="Груздева Татьяна Витальевна", callback_data="teacher_3")],
        [InlineKeyboardButton(text="Сальникова Кристина Владимировна", callback_data="teacher_4")],
        [InlineKeyboardButton(text="Шмелев Олег Валерьевич", callback_data="teacher_5")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])

    await callback.message.answer(
        "<b>Преподаватели кафедры</b>\n\nВыберите преподавателя:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    await callback.answer()

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

# === ПОЛЕЗНЫЕ КАБИНЕТЫ ===
@router.message(F.text == "Полезные кабинеты")
async def useful_rooms(message: types.Message):
    text = (
        "<b>Полезные кабинеты ИжГТУ</b>\n\n"
        "Договорной отдел\n"
        "— забрать договор об учёбе\n"
        "— подписать доп. соглашения\n"
        "Кабинет: <b>1-100а</b>\n\n"
        "Военный стол (для юношей)\n"
        "— воинский учёт, отсрочка\n"
        "Кабинет: <b>1-113</b>"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад в меню", callback_data="back_main")]
    ])

    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    
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

























