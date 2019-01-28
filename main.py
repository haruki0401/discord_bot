
import discord
from discord.ext import commands

#key
from key import DISCORD_TOKEN

from cogs import defaultcog
import riot_api
import google_search


if __name__ == '__main__':

    description = '''Hello there!! I'm Berry^^ THX for using me:D'''
    bot = commands.Bot(command_prefix = '!', description=description)
    riot = riot_api.Riot_api()
    google_search = google_search.Google_search()

    bot.add_cog(defaultcog.Defaultcog(bot, riot,google_search))

    # client = discord.Client()  "Bot class inherits discord.Cliient class, so this line does not need:D"
    bot.run(DISCORD_TOKEN)
