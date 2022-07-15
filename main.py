import keep_alive
import discord
from discord.ext import commands
import os

from special import Special

from help import Help

import asyncio


intents = discord.Intents.all()
prefix = "$"
bot = commands.Bot(command_prefix = prefix, help_command=None, intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.add_cog(Special(bot))

import logging, traceback
async def on_error(event, *args, **kwargs):
    print('Something went wrong!')
    logging.warning(traceback.format_exc())

keep_alive.keep_alive()


bot.run(os.environ["DISCORD_TOKEN"])