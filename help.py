import discord
from discord.ext import commands
from helper import make_help_embed
import re


class Help(commands.Cog):
    def __init__(self, bot, prefix):
        self.bot = bot
        self.prefix = prefix
        self.construct()

    def construct(self):
      with open('help.txt') as f:
        lines = f.readlines()
        data = {}
        catsRef = {}
        currentCategory = None
        currentCommand = None
        currentText = ""
        categoryMatch = re.compile('\{(.*?)\}')
        aliasesMatch = re.compile('\((.*?)\)')
        for line in lines:
          line = line.replace('\n','').strip()
          if line == "":
            continue
          if line == "---":
            if currentCommand:
              data[currentCategory][currentCommand] = currentText.strip()
            currentCategory = None
            currentCommand = None
            currentText = ""
          elif line == "--":
            if currentCommand:
              data[currentCategory][currentCommand] = currentText.strip()
            else:
              data[currentCategory]['desc'] = currentText.strip()
            currentCommand = None
            currentText = ""
          else:
            if not currentCategory:
              try:
                currentCategory = categoryMatch.search(line).group(1)
                data[currentCategory] = {}
                catsRef[currentCategory] = currentCategory
              except:
                print(line)
                exit()
              aliases = aliasesMatch.search(line)
              if aliases:
                for al in aliasesMatch.search(line).group(1).replace(' ','').split(','):
                  catsRef[al] = currentCategory
            else:
              if 'desc' in data[currentCategory]:
                if not currentCommand:
                  currentCommand = line
                else:
                  currentText += ' '+line
              else:
                currentText += ' '+line
        self.data = data
        self.catsRef = catsRef
        print(data)
        print(catsRef)

    @commands.command(aliases=["h", "halp"])
    async def help(self, ctx, arg: str=""):
        self.construct()
        if arg in self.catsRef:
          arg = self.catsRef[arg]
          emb = make_help_embed("Help - " + arg, self.data[arg]['desc'])
          for command, desc in self.data[arg].items():
            if command == "desc":
              continue
            if command[0] == "*":
              emb.add_field(name="$" + command[1:], value=desc + " *This command requires admin permission.*", inline=False)
            elif command[0] == '/':
              emb.add_field(name=command, value=desc, inline=False)
            else:
              emb.add_field(name="$" + command, value=desc, inline=False)
          await ctx.send(embed=emb)
        else:
            emb = make_help_embed("Help", f"gammabot is dedicated to catmath <3 forever!\nTry `" + self.prefix + "help [category]` for more detailed helps. For example, `" + self.prefix + "help points`.")
            for cat, desc in self.data.items():
              emb.add_field(name=cat, value=desc['desc'], inline=False)
            await ctx.send(embed=emb)