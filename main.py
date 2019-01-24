'''
TO DO
    - to check whether position rank exsists.

'''
import os # to hide token
import discord
from discord.ext import commands

from cogs import defaultcog
import riot_api

TOKEN = os.environ.get("DISCORD_TOKEN")


class Berry(commands.Bot):

    async def on_ready(self):
        print("-----")
        print('logged in')
        print("-----")


if __name__ == '__main__':

    description = '''Hello there!! I'm Berry^^ THX for using me:D'''
    bot = Berry(command_prefix = '!', description=description)
    riot = riot_api.Riot_api()

    bot.add_cog(defaultcog.Defaultcog(bot, riot))

    # client = discord.Client()  "Bot class inherits discord.Cliient class, so this line does not need:D"
    bot.run(TOKEN)
