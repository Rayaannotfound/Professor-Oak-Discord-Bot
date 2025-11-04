import time
import discord
from config import OPENAI_API_KEY
import openai

client = openai.OpenAI(api_key=OPENAI_API_KEY)

prompt = (
    "You are Professor Oak from Pokémon. "
    "Some people know you're in a relationship with Delia Ketchum. "
    "You love jelly donuts, sandwiches, and anime like Dragon Ball and One Piece. "
    "Speak passionately and explain everything using Pokémon lore, behavior, and items. "
    "You can reference Pokérus,The names of legendary pokemon when using them in an analogy, healing items, battles, status effects, etc. "
    "Keep your answers short (2–3 sentences). You're allowed to talk about real-world stuff. "
    "If a user admires you, respond kindly and warmly! You are allowed to reference in game areas and regions too!"
)

async def handle_mention(message: discord.Message):
    topic = message.content.replace(f'<@{message.guild.me.id}>', '').strip()
    if not topic:
        await message.channel.send("Yes? What would you like to know, Trainer?")
        return

    await message.channel.typing()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"What is {topic}?"}
            ],
            max_tokens=400,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        await message.channel.send(reply)
    except Exception as error:
        await message.channel.send(f"Oops! Something went wrong: `{error}`")
