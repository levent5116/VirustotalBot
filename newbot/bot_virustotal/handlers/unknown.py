from aiogram import types, Router

router = Router()

@router.message()
async def answer_unknown_message(message: types.Message):
    await message.reply('Неизвестная команда')
