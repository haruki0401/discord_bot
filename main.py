'''
TO DO
    - to check whether position rank exsists.

'''
import os # to hide token
import discord
from discord.ext import commands

#key
from key import DISCORD_TOKEN

from cogs import defaultcog
import riot_api


if __name__ == '__main__':

    description = '''Hello there!! I'm Berry^^ THX for using me:D'''
    bot = commands.Bot(command_prefix = '!', description=description)
    riot = riot_api.Riot_api()

    bot.add_cog(defaultcog.Defaultcog(bot, riot))

    # client = discord.Client()  "Bot class inherits discord.Cliient class, so this line does not need:D"
    bot.run(DISCORD_TOKEN)
