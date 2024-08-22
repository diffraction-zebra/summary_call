import io
import os
import sys
import logging
import asyncio

from aiogram import Dispatcher
from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message,
)

from speech_model import transcribe
from summarize import summarize


class Form(StatesGroup):
    audio = State()


api_token = os.getenv('TELEGRAM_API_TOKEN')
assert api_token
bot = Bot(token=api_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


form_router = Router()
dp = Dispatcher()
dp.include_router(form_router)

# Function to send the keyboard automatically when the user opens the chat


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    # initialize context
    await state.update_data(book=None, assessments=[], questions=[])
    # answer
    await message.answer("Добрый день, загрузите аудио для суммаризации.")
    # route
    await state.set_state(Form.audio)


@form_router.message(Form.audio)
async def audio_upload(message: Message, state: FSMContext) -> None:
    if message.audio is None:
        await message.answer('Пожалуйста загрузите аудио.')
        return

    wait_message = await message.answer('Мы уже начали обрабатывать ваше аудио.')

    # download file
    file_id = message.audio.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    # transcribe
    buffer = io.BytesIO()
    buffer.name = 'audio.mp3'
    buffer.write(file.read())
    transcription = transcribe(buffer)
    # summarize
    summary = summarize(transcription)

    await bot.delete_message(chat_id=wait_message.chat.id, message_id=wait_message.message_id)
    await message.answer(summary)

    await state.clear()


async def main():
    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
