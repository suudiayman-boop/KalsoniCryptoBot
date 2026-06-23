import os
import discord
from discord.ext import commands
from openai import OpenAI
import requests
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import feedparser
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_news_link = ""

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

    if not scheduler.running:
        scheduler.start()

@bot.command()
async def ai(ctx, *, question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    await ctx.send(response.choices[0].message.content)
@bot.command()
async def testnews(ctx):
    channel = bot.get_channel(1459589952076779695)
    await channel.send("📰 Market News test message")

@bot.command()
async def testcalendar(ctx):
    channel = bot.get_channel(1517571243769860236)
    await channel.send("📅 Economic Calendar test message")

@bot.command()
async def testrecap(ctx):
    channel = bot.get_channel(1517565567614058506)
    await channel.send("📊 Market Recap test message")
@bot.command()
async def runnews(ctx):
    await market_news()
    await ctx.send("News sent!")

scheduler = AsyncIOScheduler()

async def market_news():
    global last_news_link

    feed = feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/")

    if len(feed.entries) == 0:
        return

    news = feed.entries[0]

    keywords = [
        "bitcoin", "btc", "ethereum", "eth",
        "crypto", "forex", "stock", "nasdaq",
        "dow", "s&p", "fed", "cpi", "inflation"
    ]

    if not any(word in news.title.lower() for word in keywords):
        return

    if news.link == last_news_link:
        return

    last_news_link = news.link

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
              "content": f"""
Title: {news.title}

Qor war kooban oo market news ah.

SHARCIYO:

🚨 Qor sida warbaahin rasmi ah.

🌍 Luqad:

- 70% Somali, 30% English.
- Somali fudud oo la fahmi karo.
- Magacyada gaarka ah sida Bitcoin, Ethereum, ETF, SEC, Fed, BlackRock, Nasdaq, S&P 500 ha ku qornaadaan English.

📰 Xogta:

- Qor kaliya xaqiiqooyinka ku jira news-ka.
- Jawaabtaadu ha ku salaysnaato kaliya title-ka iyo news-ka la siiyay.
- Ha isticmaalin aqoon dibadeed ama xog kale.
- Ha ku darin xog aan news-ka ku jirin.
- Ha sameyn falanqayn, ra'yi, ama saadaal.
- Ha sharxin sababta dhacdada haddii news-ku aanu sheegin.
- Ha qorin saameynteeda haddii news-ku aanu sheegin.
- Ha qorin natiijooyin mustaqbalka ah.
- Ha qorin wax ka badan waxa news-ku xaqiijiyay.

❌ Ha isticmaalin:

- laga yaabaa
- dhici karta
- mustaqbalka
- may
- might
- could
- possibly
- likely
- expected
- probably
- perhaps

❌ Ha qorin:

- No notable updates
- No significant information
- No information available
- Major organizational reset
- Market pressure
- Investor sentiment
- Economic implications

📌 Qaybaha:

- Haddii news-ku Crypto quseeyo → Crypto qor.

- Haddii news-ku Forex quseeyo → Forex qor.

- Haddii news-ku Stocks quseeyo → Stocks qor.

- Haddii Crypto uusan ku jirin → Crypto: N/A

- Haddii Forex uusan ku jirin → Forex: N/A

- Haddii Stocks uusan ku jirin → Stocks: N/A

🎨 Emoji:

- 🚨 = Breaking News
- 🪙 = Crypto
- 💵 = Forex
- 📈 = Stocks

📝 Headline:

- Headline-ka u beddel Somali kooban.
- Ha soo celin headline-ka English haddii aan loo baahnayn.

📏 Qaab:

- Headline = 1 sadar.
- Crypto = 1 sadar ama N/A.
- Forex = 1 sadar ama N/A.
- Stocks = 1 sadar ama N/A.
- Kooban, nadiif ah, oo si fudud loo fahmi karo.

FORMAT:

🚨 BREAKING MARKET NEWS

Headline:
(1 line)

🪙 Crypto:
(1 line ama N/A)

💵 Forex:
(1 line ama N/A)

📈 Stocks:
(1 line ama N/A)
"""
        }
    ]
)

    channel = bot.get_channel(1459589952076779695)

    print(channel)

    if channel is None:
        print("CHANNEL NOT FOUND")
        return

    await channel.send(
        f"📰 MARKET NEWS\n\n{response.choices[0].message.content}"
    )

scheduler.add_job(
    market_news,
    "interval",
    minutes=5
)

async def daily_motivation():
    channel = bot.get_channel(1291313497703186454)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": """
Qor Daily Motivation.

Format:

🔥 DAILY MOTIVATION

🇺🇸 English:
(1 line)

🇸🇴 Somali:
(1 line)

💪 (1 short line)

Kooban.
Xirfad leh.
"""
        }]
    )

    await channel.send(response.choices[0].message.content)


async def trading_tip():
    channel = bot.get_channel(1517614584977035314)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": """
Qor Trading Tip.

Format:

📈 TRADING TIP

🇺🇸 English:
(1 line)

🇸🇴 Somali:
(1 line)

Kooban.
Xirfad leh.
"""
        }]
    )

    await channel.send(response.choices[0].message.content)


async def risk_management():
    channel = bot.get_channel(1517615207831306300)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": """
Qor Risk Management Tip.

Format:

🛡️ RISK MANAGEMENT

🇺🇸 English:
(1 line)

🇸🇴 Somali:
(1 line)

Kooban.
Xirfad leh.
"""
        }]
    )

    await channel.send(response.choices[0].message.content)


async def trading_psychology():
    channel = bot.get_channel(1517615839745019964)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": """
Qor Trading Psychology.

Format:

🧠 TRADING PSYCHOLOGY

🇺🇸 English:
(1 line)

🇸🇴 Somali:
(1 line)

Kooban.
Xirfad leh.
"""
        }]
    )

    await channel.send(response.choices[0].message.content)


scheduler.add_job(
    daily_motivation,
    CronTrigger(hour=10, minute=0)
)

scheduler.add_job(
    risk_management,
    CronTrigger(day_of_week="mon,tue", hour=11, minute=0)
)

scheduler.add_job(
    trading_tip,
    CronTrigger(day_of_week="wed,thu,fri", hour=12, minute=0)
)

scheduler.add_job(
    trading_psychology,
    CronTrigger(day_of_week="sat,sun", hour=13, minute=0)
)

@bot.event
async def on_message(message):
    print(f"MESSAGE RECEIVED: {message.content}")
    await bot.process_commands(message)
bot.run(DISCORD_TOKEN)
