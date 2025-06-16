import asyncio
import logging
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
import sqlite3
from config import TELEGRAM_API_TOKEN
from kinopoisk_api import get_movie_by_query
from link_Watch_Movie import get_first_google_link


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("data/history.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history (
    user_id INTEGER,
    query TEXT,
    result TEXT
)
""")
conn.commit()


@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply(
        "Я помогу найти фильмы. Напиши название, "
        "а я найду информацию!"
    )


@dp.message(Command("history"))
async def get_history(message: types.Message):
    cursor.execute("SELECT query FROM search_history WHERE user_id = ?",
                   (message.from_user.id,))
    results = cursor.fetchall()
    if results:
        history = "\n".join([r[0] for r in results])
        await message.reply(f"Ваша история:\n{history}")
    else:
        await message.reply("История поиска пуста.")


@dp.message(Command("stats"))
async def get_stats(message: types.Message):
    cursor.execute("""
        SELECT result, COUNT(*)
        FROM search_history
        WHERE user_id = ?
        GROUP BY result
        ORDER BY COUNT(*) DESC
    """, (message.from_user.id,))
    stats = cursor.fetchall()
    if stats:
        stats_message = "\n".join([f"{row[0]}: {row[1]} раз(а)"
                                   for row in stats])
        await message.reply(f"Ваша статистика:\n{stats_message}")
    else:
        await message.reply("Статистика пуста.")


@dp.message()
async def search_movie(message: types.Message):
    query = message.text
    await message.reply("Минуточку! Ищу информацию...")
    result = await get_movie_by_query(query)

    if isinstance(result, str):
        await message.reply(result)
    else:
        title, rating, poster, overview = result

        watch_link = get_first_google_link(f"{query} смотреть бесплатно")
        if not watch_link:
            watch_link = "Ссылка для просмотра не найдена."

        await message.reply_photo(
            photo=poster,
            caption=f"*{title}*\nРейтинг: {rating}\nОбзор: {overview}"
                    f"\n[Ссылка для просмотра]({watch_link})",
            parse_mode=ParseMode.MARKDOWN
        )
        cursor.execute(
            "INSERT INTO search_history (user_id, query, result)"
            " VALUES (?, ?, ?)",
            (message.from_user.id, query, title)
        )
        conn.commit()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':  # to run the bot
    asyncio.run(main())
