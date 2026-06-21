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

    if len(feed.entries) > 0:
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

Write:

Headline:
One short Somali summary only.

Impact:
Crypto:
Forex:
Stocks:

Maximum 6 lines.
70% Somali.
30% English.
No long explanation.
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
async def economic_calendar():
    channel = bot.get_channel(1517571243769860236)

    await channel.send(
        "📅 Economic Calendar\n\nCPI Tomorrow 8:30 AM EST\nForecast: 3.1%"
    )


scheduler.add_job(
    market_news,
    "interval",
    minutes=5
)
@bot.event
async def on_message(message):
    print(f"MESSAGE RECEIVED: {message.content}")
    await bot.process_commands(message)
bot.run(DISCORD_TOKEN)
