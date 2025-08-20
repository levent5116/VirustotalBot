from aiogram import Router, types, F
from aiogram.enums import ParseMode

from newbot.bot_virustotal.services.analyzer import analyze_virustotal_report
from newbot.bot_virustotal.config import *
import requests
import time
from aiogram.filters import Command
import base64


router = Router()

@router.message(Command("scan_url"))
async def cmd_scan_url(message: types.Message):
    await message.answer("🌐 Введите URL для проверки (начинается с http:// или https://)")


@router.message(F.text.startswith(('http://', 'https://')))
async def handle_url(message: types.Message):
    sent_message = await message.answer("🔍 Анализирую URL...")

    try:
        # Кодируем URL
        url_id = base64.urlsafe_b64encode(message.text.encode()).decode().strip("=")

        # Получаем отчет
        report = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers={"x-apikey": VT_KEY}
        ).json()

        result = analyze_virustotal_report(report)
        await sent_message.delete()
        await message.answer(result, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await sent_message.delete()
        await message.answer(f"⚠️ Ошибка: {str(e)}")