import discord
from discord.ext import commands

# key
from key import DISCORD_TOKEN

from cogs import defaultcog
import riot_api
import google_search

import traceback

INITIAL_EXTENSIONS = [
    'cogs.defaultcog'
]


class myBot(commands.Bot):

    # constructor
    def __init__(self, command_prefix, description):
        # pass to super class
        super().__init__(command_prefix)
        # extention cog
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    '''
    def set_id(self, temp_id: int):
        f = open("channel_id", 'w')
        f.write(str(temp_id))
        f.close
    '''

    def get_id(self):
        f = open("channel_id", 'r')
        temp_id = ''
        for line in f:
            temp_id = line
        f.close

        return temp_id

    # on_ready
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

    async def on_command_error(self, ctx, exception):
        print('error!')
        # print(defaultcog.set_channel_id)
        if ctx.message.channel.id == int(self.get_id()):
            if isinstance(exception, commands.errors.CommandNotFound):
                embed = discord.Embed(
                    description="There is no command you entered.",
                    color=0xeee657)
                await ctx.send(embed=embed)


if __name__ == '__main__':

    description = '''Hello there!! I'm Berry^^ THX for using me:D'''
    bot = myBot(command_prefix='!', description=description)
    riot = riot_api.Riot_api()
    google_search = google_search.Google_search()

    # bot.add_cog(defaultcog.Defaultcog(bot, google_search))

    # client = discord.Client()  "Bot class inherits discord.Cliient class, so
    # this line does not need:D"
    bot.run(DISCORD_TOKEN)
