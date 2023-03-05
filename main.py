import config
from loguru import logger
import openai
import asyncio
from gpytranslate import Translator
from aiogram import Bot, Dispatcher, executor, types

logger.add("file.log", level="INFO")

t = Translator()

openai.api_key = config.OPENAI_TOKEN

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Я ChatGPT бот. Я готов отвечать на ваши сообщения, начинающиеся с '!'.")


@dp.message_handler(lambda message: message.text.startswith("!"))
async def gpt_answer(message: types.Message):
    model_engine = "text-davinci-003"
    max_tokens = 128
    prompt = await t.translate(message.text, targetlang="en")
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt.text,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    await message.answer("ChatGPT: Генерирую ответ ...")
    translated_result = await t.translate(completion.choices[0].text, targetlang="ru")
    await message.answer(translated_result.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# import config
# import logging
# import openai
# import asyncio
# from gpytranslate import Translator

# from aiogram import Bot, Dispatcher, executor, types

# # log
# logging.basicConfig(level=logging.INFO)

# # init translator
# t = Translator()

# # init openai
# openai.api_key = config.OPENAI_TOKEN

# # init aiogram
# bot = Bot(token=config.TOKEN)
# dp = Dispatcher(bot)


# @dp.message_handler()
# async def gpt_answer(message: types.Message):
#     # await message.answer(message.text)

#     model_engine = "text-davinci-003"
#     max_tokens = 128  # default 1024
#     prompt = await t.translate(message.text, targetlang="en")
#     completion = openai.Completion.create(
#         engine=model_engine,
#         prompt=prompt.text,
#         max_tokens=max_tokens,
#         temperature=0.5,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     await message.answer("ChatGPT: Генерирую ответ ...")
#     translated_result = await t.translate(completion.choices[0].text, targetlang="ru")
#     await message.answer(translated_result.text)

# # run long-polling
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)
