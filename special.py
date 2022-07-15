import discord
from discord.ext import commands
import json
import random
import math
import time
from pathlib import Path
import requests
import os
from helper import make_embed

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  




    @commands.command(aliases=[])
    async def test(self, ctx):
        guild = ctx.guild.id
        for member in ctx.guild.members:
            img_data = requests.get(member.avatar_url).content
            with open(str(member.id)+'.jpg', 'wb') as handler:
                handler.write(img_data)
        await ctx.send(guild)

      


