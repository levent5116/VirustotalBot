from aiogram.filters import Command
from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Создаём кнопки
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/scan_url")],
        [KeyboardButton(text="/scan_file")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False  # Клавиатура остаётся
)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🛡️ Бот для проверки файлов и URL через VirusTotal\n\n"
        "Команды:\n"
        "/scan_url - проверить сайт\n"
        "/scan_file - проверить файл" , reply_markup=keyboard
    )

# Обработка нажатий на кнопки
@router.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "scan_url":
        await callback.message.edit_text("🌐 Отправьте ссылку (URL) для проверки:")
    elif callback.data == "scan_file":
        await callback.message.edit_text("📎 Отправьте файл для проверки:")

    # Убираем индикатор загрузки
    await callback.answer()