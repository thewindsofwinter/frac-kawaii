import discord

footer_url = "https://cdn.discordapp.com/attachments/729794136001085491/881965839337799680/ezgif.com-gif-maker_1.gif"

footer_text = 'made with (⁄˘⁄ ⁄ ω⁄ ⁄ ˘⁄)♡ by very'

def make_embed(title,description):
  return discord.Embed(color=0xffd012,title=title,description=description).set_author(name='very\'s osu bot',icon_url='https://cdn.discordapp.com/avatars/876655027769475082/a63b54db830823656bd8f5ace4e7d5d5.png?size=1024').set_footer(text=footer_text,icon_url=footer_url)

def make_greed_embed(title,description):
  return discord.Embed(color=0xffd012,title=title,description=description).set_author(name='gammabot - greed control',url='https://discord.gg/QJDrpHSdjq',icon_url='https://cdn.discordapp.com/attachments/534001679675424779/881970143071203388/cathelp.png').set_footer(text=footer_text,icon_url=footer_url)


def make_help_embed(title, description):
  return discord.Embed(color=0x0094ff,title=title,description=description).set_author(name='gammabot - help',url='https://discord.gg/QJDrpHSdjq',icon_url='https://cdn.discordapp.com/attachments/534001679675424779/881971955081838692/cathelp.png').set_footer(text=footer_text,icon_url=footer_url)
