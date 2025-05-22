import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

WELCOME_TEXT = (
    "Чувствуете?.. \n\n"
    "Еще с юношества теплое время ассоциируется у нас с самой нежной, и в то же время, сумасшедшей любовью\n\n"
    "Этим летом мы взяли на себя миссию возродить это ощущение через цветы\n\n"
    "Это особенные букеты. В каждом лежит воспоминание о первой любви, "
    "которым наши флористы от всего сердца решили с вами поделиться"
)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🌹 Получить каталог летней коллекции", callback_data="catalog")
    await message.answer(WELCOME_TEXT, reply_markup=keyboard.as_markup())

@dp.callback_query(F.data == "catalog")
async def send_catalog(callback: types.CallbackQuery):
    media_group = []
    for i in range(1, 10):
        photo_path = f"media/{i}.jpg"
        if os.path.exists(photo_path):
            photo = FSInputFile(photo_path)
            if i == 1:
                media_group.append(
                    types.InputMediaPhoto(
                        media=photo,
                        caption="Увидели тот, который отражает Ваши чувства?\n\nПрисылайте его фото на @larosemos и мы оформим для Вас доставку"
                    )
                )
            else:
                media_group.append(types.InputMediaPhoto(media=photo))
    await bot.send_media_group(chat_id=callback.message.chat.id, media=media_group)
    await callback.answer()

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
