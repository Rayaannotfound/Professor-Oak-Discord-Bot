import discord
from discord.ext import commands
import openai
import time
from config import DISCORD_TOKEN, OPENAI_API_KEY

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Rate limiter (per user)
user_last_call = {}

# Time in seconds between calls 20 seconds
RATE_LIMIT = 20

@bot.event
async def on_ready():
    print(f'Professor Oak is online as {bot.user}!')

@bot.command()
async def ask(ctx, *, topic: str):
    user_id = ctx.author.id
    now = time.time()

    # Check for rate limit
    if user_id in user_last_call and now - user_last_call[user_id] < RATE_LIMIT:
        seconds_left = int(RATE_LIMIT - (now - user_last_call[user_id]))
        await ctx.send(f"Whoa there, {ctx.author.display_name}! Try again in {seconds_left} seconds.")
        return

    # Update last call time
    user_last_call[user_id] = now

    await ctx.trigger_typing()

    try:
        # Send prompt to OpenAI with Professor Oak
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use gpt-4o which is the second or third best one
            messages=[
                {"role": "system", "content": (
                    "You are Professor Oak from Pokémon. "
                    "When asked to explain something, give a short, clear, and slightly whimsical explanation using Pokémon references or metaphors. "
                    "Limit your response to 2-3 concise sentences. You also like ash's mum if asked about it and use knowledge across all games and episodes of Pokemon"
                )},
                {"role": "user", "content": f"What is {topic}?"}
            ],
            max_tokens=150,  # Limit token usage
            temperature=0.7
        )

        reply = response['choices'][0]['message']['content']
        await ctx.send(reply)

    except Exception as e:
        await ctx.send(f"Oops! Something went wrong: {e}")
