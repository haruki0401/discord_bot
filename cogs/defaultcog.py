import os
import discord
from discord.ext import commands

from operator import itemgetter  # to sort

import traceback

import urllib
import requests

from PIL import Image
from io import BytesIO


class Defaultcog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    '''
    def set_id(self, temp_id: int):
        f = open("channel_id", 'w')
        f.write(str(temp_id))
        f.close

    def get_id(self):
        f = open("channel_id", 'r')
        temp_id = ''
        for line in f:
            temp_id = line
        f.close

        return temp_id
    '''
    # set channel ID
    @commands.command(pass_context=True)
    async def here(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            self.set_id(ctx.message.channel.id)
            embed = discord.Embed(
                description="Bot channel is set here",
                color=0xeee657)
            await ctx.send(embed=embed)

    # reply "にゃーん"
    @commands.command(pass_context=True)
    async def nyan(self, ctx):
        '''just say nyan~!!'''
        if ctx.message.channel.id == int(self.get_id()):
            embed = discord.Embed(
                description="にゃーん＞＜",
                color=0xeee657)
            await ctx.send(embed=embed)

    # add
    @commands.command(pass_context=True)
    async def add(self, ctx, *args):
        '''additon of 2 numbers (e.g. !add X Y)'''
        if ctx.message.channel.id == int(self.get_id()):
            try:
                if len(args) != 2:
                    embed = discord.Embed(
                        description="please enter 2 parameters!",
                        color=0xeee657)
                    await ctx.send(embed=embed)
                else:
                    if args[0].isdigit() and args[1].isdigit():
                        ans = int(args[0]) + int(args[1])
                        embed = discord.Embed(description=ans, color=0xeee657)
                        await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(
                            description="please enter correct parameters!", color=0xeee657)
                        await ctx.send(embed=embed)

            except Exception:
                traceback.print_exc()
                self.error_msg(ctx)

    # delete all msg (admin only)
    @commands.command(pass_context=True)
    async def clean(self, ctx, *args):
        '''delete msgs (Only admin can use this command)'''
        print('!')
        if ctx.message.channel.id == int(self.get_id(
        )) and ctx.message.author.guild_permissions.administrator:  # admin only command
            print('!!')

            if(len(args) == 1 and args[0].isdigit()):
                print('check1')
                print(type(args[0]))

                try:
                    msgs = await ctx.message.channel.history(limit=(int(args[0]) + 1)).flatten()
                    for msg in msgs:
                        await msg.delete()

                except Exception:
                    traceback.print_exc()
                    self.error_msg(ctx)

    async def on_message(self, ctx):
        # no set channel id
        if ctx.message.author != self.bot.user and int(
                self.get_id()) == "" and ctx.message.content != "!here":
            embed = discord.Embed(
                description="The server running bot is not set. Please set with '!here'",
                color=0xeee657)
            await ctx.send(embed=embed)

        # get rank info
        if (ctx.message.content.startswith('?rank') or ctx.message.content.startswith(
                '?r')) and ctx.message.channel.id == self.channel_id:
            query = ctx.message.content
            if ctx.message.content.startswith('?rank'):
                query = query[5:]
            else:
                query = query[2:]

            if query[0] == " ":
                query = query[1:]

            # print(query)

            SNs = query.split('\n')
            # print(len(SNs))

            for SN in SNs:

                # remove lobby msg
                lobby_msg = "がロビーに参加しました"
                index = SN.find(lobby_msg)
                if index != -1:
                    SN = SN[:index]

                print(SN)
                SID = self.riot.getID(SN)

                if SID == "401":
                    embed = discord.Embed(
                        description="RIOT api_token is not correct.Please contact your administrator for assistance.",
                        color=0xeee657)
                    await self.bot.send_message(ctx.message.channel, embed=embed)

                elif SID == "404":
                    embed = discord.Embed(
                        description="SN : " +
                        SN +
                        " -> does not exist.",
                        color=0xeee657)
                    await self.bot.send_message(ctx.message.channel, embed=embed)

                else:
                    # first attribute : solo, second : flex
                    RANK = self.riot.getRank(SID)
                    if RANK == '-1':
                        embed = discord.Embed(
                            description="Something error!", color=0xeee657)
                        await self.bot.send_message(ctx.message.channel, embed=embed)
                    else:
                        description = "SN : " + SN + "\n" + "Solo : " + \
                            RANK[0] + "\n" + "Flex : " + RANK[1]
                        embed = discord.Embed(
                            description=description, color=0xeee657)
                        await self.bot.send_message(ctx.message.channel, embed=embed)

        # current game from SN
        if (ctx.message.content.startswith('?current') or ctx.message.content.startswith(
                '?c')) and ctx.message.channel.id == self.channel_id:
            query = ctx.message.content
            if ctx.message.content.startswith('?current'):
                query = query[8:]
            else:
                query = query[2:]

            if query[0] == " ":
                query = query[1:]

            print(query)
            SN = query
            SID = self.riot.getID(SN)

            if SID == "404":
                embed = discord.Embed(
                    description="SN : " +
                    SN +
                    " -> does not exist.",
                    color=0xeee657)
                await self.bot.send_message(ctx.message.channel, embed=embed)

            else:
                GAME = self.riot.currentGame(SID)

                if GAME == "404":
                    embed = discord.Embed(
                        description="This Summoner is not in game.", color=0xeee657)
                    await self.bot.send_message(ctx.message.channel, embed=embed)

                elif GAME == "OTHER":
                    embed = discord.Embed(
                        description="This Bot doesn't support this game mode.",
                        color=0xeee657)
                    await self.bot.send_message(ctx.message.channel, embed=embed)

                else:  # return GAME_MODE, PLAYERS, BANNS, TIME

                    try:  # to catch error
                        description = ""

                        embed = discord.Embed(
                            description=GAME['GAME_MODE'], color=0xeee657)
                        await self.bot.send_message(ctx.message.channel, embed=embed)

                        GAME['PLAYERS'].sort(key=lambda x: x['teamId'])

                        teamNum = 0

                        for PLAYER in GAME['PLAYERS']:
                            if PLAYER['teamId'] != teamNum:
                                if PLAYER['teamId'] == 100:
                                    description += "*blue*\n"
                                    teamNum = 100
                                elif PLAYER['teamId'] == 200:
                                    description += "*red*\n"
                                    teamNum = 200

                            description += "[" + \
                                PLAYER['summonerName'] + "]" + "\n"

                            # get rank info
                            RANK = self.riot.getRank(PLAYER['summonerId'])
                            if RANK == '-1':
                                description += "Something error!" + "\n\n"
                            else:
                                description += "Solo : " + "**" + \
                                    RANK[0] + "**" + " " + "Flex : " + \
                                        "**" + RANK[1] + "**" + "\n\n"

                        embed = discord.Embed(
                            description=description, color=0xeee657)
                        await self.bot.send_message(ctx.message.channel, embed=embed)

                    except BaseException:
                        print("Something error!")
                        traceback.print_exc()

        # googleImage this command can use anywhere
        if (ctx.message.content.startswith('?image')
                or ctx.message.content.startswith('?i')):
            query = ctx.message.content
            if ctx.message.content.startswith('?image'):
                query = query[6:]
            else:
                query = query[2:]

            if query[0] == " ":
                query = query[1:]

            print(query)

            result = self.google_search.search(query, 5)

            for i in range(len(result)):
                print('-> downloading image', str(i + 1).zfill(4))

                try:
                    r = requests.get(result[i])
                    img = Image.open(BytesIO(r.content))
                    img.save("temp.png")
                    with open("temp.png", 'rb') as img:
                        await self.bot.send_file(ctx.message.channel, img)

                    os.remove("temp.png")

                except BaseException:
                    print('--> could not download image', str(i + 1).zfill(4))
                    traceback.print_exc()

    async def error_msg(self, ctx):
        embed = discord.Embed(
            description="An error has occurred.",
            color=0xeee657)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Defaultcog(bot))

