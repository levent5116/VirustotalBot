from aiogram import Bot, Dispatcher
from config import *
from handlers.basic_commands import router as commands_router
from handlers.file_handlers import router as files_router
from handlers.unknown import router as unknown_router
from handlers.url_handlers import router as url_router
import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  

# Подключаем роутеры  
dp.include_router(commands_router)  
dp.include_router(files_router)
dp.include_router(url_router)
dp.include_router(unknown_router)

async def main():  
    await dp.start_polling(bot)

if __name__ == "__main__":  
    asyncio.run(main())
