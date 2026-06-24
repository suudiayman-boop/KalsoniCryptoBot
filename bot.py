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

🚨 QORAALKA WARARKA

- Isticmaal af Soomaali fudud oo dabiici ah.
- Qor sida qof Soomaali ah uu war u sheegayo.
- Ha isticmaalin erayo adag.
- Ha isticmaalin erayo is khilaafaya.
- Ha isticmaalin jumlado dhaadheer.
- Qof walba ha fahmi karo marka uu akhriyo.

📰 XOGTA

- Qor kaliya waxa news-ku sheegay.
- Ha ku darin fikrad adiga kuu gaar ah.
- Ha ku darin falanqayn.
- Ha ku darin saadaal.
- Ha ku darin sabab aan news-ku sheegin.
- Ha beddelin macnaha news-ka.

❌ HA ISTICMAALIN

- laga yaabaa
- dhici karta
- mustaqbalka
- u baahan yahay
- ku taliyay
- istiraatiijiyad
- falanqayn
- aragti
- cadaadis suuqa
- saameyn dhaqaale
- investor sentiment
- market pressure

🗣️ AF SOOMAALI FUDUD

❌ Trump wuxuu sheegay in heshiiska nabadda ee Iran uu saameyn weyn ku yeelan karo dhaqaalaha caalamka.

✅ Trump wuxuu sheegay in heshiiska Iran la gaaray, Strait of Hormuz-na dib loo furay.

❌ CryptoQuant ayaa ka hadashay istiraatiijiyadda Michael Saylor.

✅ CryptoQuant ayaa sheegtay in Michael Saylor uu sii iibsanayo Bitcoin.

❌ Bitcoin ayaa wajahaya cadaadis suuqa.

✅ Bitcoin qiimihiisu hoos ayuu u dhacay.

📌 QAACIDADA

- Hal fikrad = hal jumlad.
- Hal jumlad = hal macne.
- Qoraalka ha noqdo gaaban.
- Qoraalka ha noqdo cad.
- Qoraalka ha noqdo fudud.

FORMAT

🚨 WAR CUSUB

Headline:
(1 sadar)

🪙 Crypto:
(1 sadar ama N/A)

💵 Forex:
(1 sadar ama N/A)

📈 Stocks:
(1 sadar ama N/A)

Qor sida warbaahin rasmi ah.
Qor af Soomaali fudud.
Qor xaqiiqooyinka kaliya.
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

    await channel.send(
    f"@everyone\n\n{response.choices[0].message.content}"
)

scheduler.add_job(
    daily_motivation,
    CronTrigger(hour=8, minute=30)
)

scheduler.add_job(
    risk_management,
    CronTrigger(day_of_week="mon,tue", hour=12, minute=0)
)

scheduler.add_job(
    trading_tip,
    CronTrigger(day_of_week="wed,thu,fri", hour=13, minute=0)
)

scheduler.add_job(
    trading_psychology,
    CronTrigger(day_of_week="sat,sun", hour=11, minute=0)
)

@bot.command()
async def testmotivation(ctx):
    await daily_motivation()
    await ctx.send("Motivation sent!")

@bot.command()
async def testrisk(ctx):
    await risk_management()
    await ctx.send("Risk Management sent!")

@bot.command()
async def testtip(ctx):
    await trading_tip()
    await ctx.send("Trading Tip sent!")

@bot.command()
async def testpsychology(ctx):
    await trading_psychology()
    await ctx.send("Psychology sent!")

@bot.event
async def on_message(message):
    print(f"MESSAGE RECEIVED: {message.content}")
    await bot.process_commands(message)
bot.run(DISCORD_TOKEN)
