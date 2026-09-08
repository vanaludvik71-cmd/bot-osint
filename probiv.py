import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = "import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = "8982718112:AAEgYsZTFCLHsInKd0M1rypyHB12ocDooV6"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Перевірка витоків через LeakCheck API (за запитом)
async def check_leakcheck(target: str, client: httpx.AsyncClient):
    # Публічний ендпоінт для швидкого аналізу витоків
    url = f"https://leakcheck.io/api/public?check={target}"
    try:
        response = await client.get(url, timeout=7.0)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("sources"):
                sources = ", ".join([s.get("name", "Unknown") for s in data.get("sources", [])])
                return f"⚠️ <b>Знайдено у витоках баз:</b> {data.get('found', 0)}\n📁 <b>Джерела/Бази:</b> {sources}"
            elif data.get("found") == 0:
                return "✅ У публічних базах витоків паролів/даних не знайдено."
    except Exception:
        pass
    return "❌ Не вдалося отримати відповідь від сервісу баз."

# 2. Пошук профілів у соцмережах та форумах
TARGET_SITES = {
    "GitHub Profile": "https://github.com/{}",
    "Telegram Profile": "https://t.me/{}",
    "Steam ID": "https://steamcommunity.com/id/{}",
    "Reddit User": "https://www.reddit.com/user/{}",
    "Chess.com": "https://www.chess.com/member/{}",
}

async def check_site(site: str, url_template: str, username: str, client: httpx.AsyncClient):
    url = url_template.format(username)
    try:
        response = await client.get(url, timeout=4.0, follow_redirects=True)
        if response.status_code == 200:
            return f"🟢 <b>{site}</b>: {url}"
    except Exception:
        pass
    return None

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🔎 <b>OSINT Search Bot</b>\n\n"
        "Надішли мені:\n"
        "• Нікнейм (наприклад: <code>alex_dev</code>)\n"
        "• Email (наприклад: <code>target@gmail.com</code>)\n"
        "• Номер телефону (наприклад: <code>+380991234567</code>)",
        parse_mode="HTML"
    )

@dp.message()
async def search_query(message: types.Message):
    query = message.text.strip()
    if not query:
        return

    status_msg = await message.answer(f"🔍 Проводжу аналіз по базах для: <code>{query}</code>...", parse_mode="HTML")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    async with httpx.AsyncClient(headers=headers) as client:
        # Одночасний пошук по сайтах та базах витоків
        site_tasks = [check_site(site, tmpl, query, client) for site, tmpl in TARGET_SITES.items()]
        leak_task = check_leakcheck(query, client)

        site_results, leak_result = await asyncio.gather(
            asyncio.gather(*site_tasks),
            leak_task
        )

    found_sites = [r for r in site_results if r]

    # Формування підсумкового звіту
    report = [f"📊 <b>Звіт OSINT для:</b> <code>{query}</code>\n"]

    if leak_result:
        report.append("<b>1. Перевірка баз витоків (LeakCheck):</b>")
        report.append(leak_result)
        report.append("")

    report.append("<b>2. Знайдені акаунти та профілі:</b>")
    if found_sites:
        report.extend(found_sites)
    else:
        report.append("Нічого не знайдено у відкритих профілях.")

    await status_msg.edit_text("\n".join(report), parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# 1. Перевірка витоків через LeakCheck API (за запитом)
async def check_leakcheck(target: str, client: httpx.AsyncClient):
    # Публічний ендпоінт для швидкого аналізу витоків
    url = f"https://leakcheck.io/api/public?check={target}"
    try:
        response = await client.get(url, timeout=7.0)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("sources"):
                sources = ", ".join([s.get("name", "Unknown") for s in data.get("sources", [])])
                return f"⚠️ <b>Знайдено у витоках баз:</b> {data.get('found', 0)}\n📁 <b>Джерела/Бази:</b> {sources}"
            elif data.get("found") == 0:
                return "✅ У публічних базах витоків паролів/даних не знайдено."
    except Exception:
        pass
    return "❌ Не вдалося отримати відповідь від сервісу баз."


# 2. Пошук профілів у соцмережах та форумах
TARGET_SITES = {
    "GitHub Profile": "https://github.com/{}",
    "Telegram Profile": "https://t.me/{}",
    "Steam ID": "https://steamcommunity.com/id/{}",
    "Reddit User": "https://www.reddit.com/user/{}",
    "Chess.com": "https://www.chess.com/member/{}",
}


async def check_site(site: str, url_template: str, username: str, client: httpx.AsyncClient):
    url = url_template.format(username)
    try:
        response = await client.get(url, timeout=4.0, follow_redirects=True)
        if response.status_code == 200:
            return f"🟢 <b>{site}</b>: {url}"
    except Exception:
        pass
    return None


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🔎 <b>OSINT Search Bot</b>\n\n"
        "Надішли мені:\n"
        "• Нікнейм (наприклад: <code>alex_dev</code>)\n"
        "• Email (наприклад: <code>target@gmail.com</code>)\n"
        "• Номер телефону (наприклад: <code>+380991234567</code>)",
        parse_mode="HTML"
    )


@dp.message()
async def search_query(message: types.Message):
    query = message.text.strip()
    if not query:
        return

    status_msg = await message.answer(f"🔍 Проводжу аналіз по базах для: <code>{query}</code>...", parse_mode="HTML")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    async with httpx.AsyncClient(headers=headers) as client:
        # Одночасний пошук по сайтах та базах витоків
        site_tasks = [check_site(site, tmpl, query, client) for site, tmpl in TARGET_SITES.items()]
        leak_task = check_leakcheck(query, client)

        site_results, leak_result = await asyncio.gather(
            asyncio.gather(*site_tasks),
            leak_task
        )

    found_sites = [r for r in site_results if r]

    # Формування підсумкового звіту
    report = [f"📊 <b>Звіт OSINT для:</b> <code>{query}</code>\n"]

    if leak_result:
        report.append("<b>1. Перевірка баз витоків (LeakCheck):</b>")
        report.append(leak_result)
        report.append("")

    report.append("<b>2. Знайдені акаунти та профілі:</b>")
    if found_sites:
        report.extend(found_sites)
    else:
        report.append("Нічого не знайдено у відкритих профілях.")

    await status_msg.edit_text("\n".join(report), parse_mode="HTML")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())