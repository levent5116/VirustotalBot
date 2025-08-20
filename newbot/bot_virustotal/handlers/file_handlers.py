from aiogram import Router, types, F
from aiogram.enums import ParseMode

from newbot.bot_virustotal.services.analyzer import analyze_virustotal_report
from newbot.bot_virustotal.config import *
import requests
import time
from aiogram.filters import Command


router = Router()

@router.message(Command("scan_file"))
async def cmd_scan_file(message: types.Message):
    await message.answer("📎 Отправьте файл для проверки")


@router.message(F.document)
async def handle_file(message: types.Message):
    sent_message = await message.answer("🔍 Анализирую файл...")

    try:
        # Получаем файл
        file = await message.bot.get_file(message.document.file_id)
        file_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}"

        # Отправляем в VirusTotal
        with requests.get(file_url, stream=True) as f:
            response = requests.post(
                "https://www.virustotal.com/api/v3/files",
                headers={"x-apikey": VT_KEY},
                files={"file": (message.document.file_name, f.raw)}
            )

        analysis_id = response.json()["data"]["id"]

        # Ждём завершения анализа
        for _ in range(30):
            time.sleep(10)
            report = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers={"x-apikey": VT_KEY}
            ).json()

            if report.get("data", {}).get("attributes", {}).get("status") == "completed":
                result = analyze_virustotal_report(report)
                await sent_message.delete()
                return await message.answer(result, parse_mode=ParseMode.MARKDOWN)

        await sent_message.delete()
        await message.answer("⏰ Время ожидания истекло")

    except Exception as e:
        await sent_message.delete()
        await message.answer(f"⚠️ Ошибка: {str(e)}")


