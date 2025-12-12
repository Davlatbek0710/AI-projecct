import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BufferedInputFile
from table_image import make_table_png

from ollama_client import ask_model_with_examples
from table_image import make_table_png

BOT_TOKEN = "your-telegram-bot-token"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def handle_message(message: Message):
    user_text = message.text.strip()

    
    try:
        nums = [int(x) for x in user_text.split()]
        if len(nums) < 2:
            raise ValueError
        capacity = nums[0]
        items = nums[1:]
    except Exception:
        await message.answer("Write numbers by space, example:\n400 333 200 188 176 100 98 78 68 55")
        return

    model_input = f"Capacity: {capacity}. Items: " + ", ".join(map(str, items))

    await message.answer("Asking the model for optimal solution...")

    try:
        result = ask_model_with_examples(model_input)
        bins = result["bins"]
    except Exception as e:
        await message.answer(f"Error in model request:\n{e}")
        return

    img_bytes = make_table_png(bins)
    photo = BufferedInputFile(img_bytes.getvalue(), filename="bins.png")
    await message.answer_photo(photo=photo, caption="Solution of Cloud LLM")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("INFO: Bot started")
    asyncio.run(main())