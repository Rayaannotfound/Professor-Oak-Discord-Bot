import discord
import time
from discord.ext import commands
from config import RATE_LIMIT_SECONDS
from handlers.oak import handle_mention
from utils.rate_limit import is_rate_limited


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
user_last_call = {}

@bot.event
async def on_ready():
    print(f"Professor Oak is online as {bot.user}!")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        if is_rate_limited(user_last_call, message.author.id, RATE_LIMIT_SECONDS):
            seconds = int(RATE_LIMIT_SECONDS - (time.time() - user_last_call[message.author.id]))
            await message.channel.send(
                f"Whoa there, {message.author.display_name}! Try again in {seconds} seconds."
            )
            return

        user_last_call[message.author.id] = time.time()
        await handle_mention(message)

    await bot.process_commands(message)
