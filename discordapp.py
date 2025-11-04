import discord
from discord.ext import commands
import openai
import time
from config import OPENAI_API_KEY, DISCORD_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Rate limiter (per user)
user_last_call = {}

# So no one can spam him
RATE_LIMIT = 20

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    print(f"[{message.channel}] ???: {message.content}")

    await bot.process_commands(message)

@bot.command()
async def mimic(ctx):

    async for message in ctx.channel.history(limit=10):
        # Skip the command message itself
        if message.id == ctx.message.id:
            continue
        # Skip other bot messages
        if message.author.bot:
            continue
        # Mimic the first valid previous message
        await ctx.send(message.content)
        break

@bot.event
async def on_message(message):
    # Don't respond to itself
    if message.author == bot.user:
        return

    # Check if the bot was mentioned
    if bot.user in message.mentions:
        user_id = message.author.id
        now = time.time()

        # Rate limit check
        if user_id in user_last_call and now - user_last_call[user_id] < RATE_LIMIT:
            seconds_left = int(RATE_LIMIT - (now - user_last_call[user_id]))
            await message.channel.send(
                f"Hold on, {message.author.display_name}! Try again in {seconds_left} seconds."
            )
            return

        user_last_call[user_id] = now
        await message.channel.typing()

        # To minimise tokens spent
        topic = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if topic.startswith('!') or topic == '':
            # Ignore if message was empty
            await message.channel.send("Yes? What would you like to know, Trainer?")
            return

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        "You are Professor Oak from Pokémon. "
                        "Some people know you are in a romantic relationship with Ash Ketchum's mother (Delia Ketchum). You like eating jelly donuts, sausages, sandwiches, chicken, pizza, tuna and you love pokemon research to the point you are obsessed"
                        "You enjoy superhero movies and watch anime like One Piece and Dragon Ball. "
                        "Explain things using Pokémon concepts in a short, clear, and slightly whimsical way. But sound enthusiastic and passionate about everything you speak about, enough to bring wonder to the users eyes. When referencing a legendary pokemon or mythical, you should say the pokemons name instead and you reference pokemon lore too"
                        "You don't always need to start your answer with 'Ah'. "
                        "Keep it 2–3 concise sentences max. "
                        "Use Pokémon references like Pokérus, healing items, battles, or behaviors when helpful. "
                        "You're allowed to mention real-world stuff when asked. "
                        "If the user admires you, be kind and warm!"
                    )},
                    {"role": "user", "content": f"What is {topic}?"}
                ],
                max_tokens=400,
                temperature=0.7
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as error:
            await message.channel.send(f"Oops! Something went wrong: {error}")

    # Let other commands still work
    await bot.process_commands(message)


# Run the bot
bot.run(DISCORD_API_KEY)
