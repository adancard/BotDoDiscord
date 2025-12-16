import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import timedelta
import re
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

keep_alive()

ALVO_ID = 476134691767058453  # Miguel 😈

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

padrao_nintendo = re.compile(r"\bnintend\w*", re.IGNORECASE)

@bot.event
async def on_ready():
    print(f"Ligado e operante, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Bem-vindo ao servidor, {member.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if padrao_nintendo.search(message.content):
        membro = message.guild.get_member(ALVO_ID)

        await message.channel.send(
            f"{message.author.mention} Nesse servidor não 😡 "
            "só por isso o Miguel vai tomar castigo"
        )

        if membro:
            if not membro.is_timed_out():
                await membro.timeout(
                    timedelta(minutes=1440),
                    reason="Palavra proibida"
                )
            else:
                await message.channel.send("O cara já tá mutado pô 😅")

    # Quando o bot for mencionado
    if bot.user in message.mentions:
        await message.channel.send("É verdade, eu confirmo")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
