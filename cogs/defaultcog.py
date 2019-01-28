import discord
from discord.ext import commands

import traceback


class Defaultcog(commands.Bot):
    channel_id = ""

    def __init__(self, bot, riot):
        self.bot = bot
        self.riot = riot


    async def on_ready(self):
        print("-----")
        print('logged in')
        print("-----")


    #enter command that does not exist
    async def on_command_error(self, exception: Exception, ctx: commands.Context):
        if ctx.message.channel.id == self.channel_id:
            channel = ctx.message.channel
            if isinstance(exception, commands.CommandNotFound):
                embed = discord.Embed(description = "There is no command you entered.", color=0xeee657)
                await self.bot.send_message(ctx.message.channel, embed = embed)

    # set channel ID
    @commands.command(pass_context=True)
    async def here(self,ctx):
        if ctx.message.author.server_permissions.administrator:
            self.channel_id = ctx.message.channel.id
            embed = discord.Embed(description = "Bot channel is set here", color=0xeee657)
            await self.bot.say(embed = embed)


    # reply "にゃーん"
    @commands.command(pass_context=True)
    async def nyan(self,ctx):
        '''just say nyan~!!''' 
        if ctx.message.channel.id == self.channel_id:
            embed = discord.Embed(description = "にゃーん＞＜", color=0xeee657)
            await self.bot.say(embed = embed)

    # add
    @commands.command(pass_context=True)
    async def add(self, ctx, *args):
        '''additon of 2 numbers (e.g. !add X Y)'''
        if ctx.message.channel.id == self.channel_id:
            if len(args) != 2:
                embed = discord.Embed(description = "please enter 2 parameters!", color=0xeee657)
                await self.bot.say(embed = embed)
            else:
                if args[0].isdigit() and args[1].isdigit():
                    ans = int(args[0]) + int(args[1])
                    embed = discord.Embed(description = ans, color=0xeee657)
                    await self.bot.say(embed = embed) 
                
                else:
                    embed = discord.Embed(description = "please enter correct parameters!", color=0xeee657)
                    await self.bot.say(embed = embed) 
        
    # delete all msg (admin only)
    @commands.command(pass_context=True)
    async def clean(self, ctx, *args):
        '''delete all msg (Only admin can usethis command)'''
        if ctx.message.channel.id == self.channel_id and ctx.message.author.server_permissions.administrator: # admin only command
            
            if(len(args) == 0):
                #all delete
                clean_flag = True
                while (clean_flag):
                    msgs = [msg async for msg in self.bot.logs_from(ctx.message.channel)]
                    if len(msgs) > 1: # 1発言以下でdelete_messagesするとエラーになる
                        await self.bot.delete_messages(msgs)
                    else:
                        clean_flag = False
                        embed = discord.Embed(description = "deleted all msgs!!", color=0xeee657)
                        await self.bot.say(embed = embed)
            
            elif(len(args) == 1 and args[0].isdigit()):
                msgs = [msg async for msg in self.bot.logs_from(ctx.message.channel, limit = int(args[0]) + 1)]
                await self.bot.delete_messages(msgs)
                            
    async def on_message(self, message):
        #no set channel id
        if message.author != self.bot.user and self.channel_id == "" and message.content != "!here":
            embed = discord.Embed(description = "The server running bot is not set. Please set with '!here'", color=0xeee657)
            await self.bot.send_message(message.channel, embed = embed)


        #get rank info
        if (message.content.startswith('?rank') or message.content.startswith('?r')) and message.channel.id == self.channel_id:
            query = message.content
            if message.content.startswith('?rank'):
                query = query[5:]
            else:
                query = query[2:]

            if query[0] == " ":
                query = query[1:]

            #print(query)

            SNs = query.split('\n')
            #print(len(SNs))

            for SN in SNs:

                #remove lobby msg
                lobby_msg = "がロビーに参加しました"
                index = SN.find(lobby_msg)
                if index != -1:
                    SN = SN[:index]

                print(SN)
                SID = self.riot.getID(SN)   
                
                
                if SID == "401":
                    embed = discord.Embed(description = "RIOT api_token is not correct.Please contact your administrator for assistance.", color=0xeee657)
                    await self.bot.send_message(message.channel, embed = embed)
                

                elif SID == "404":
                    embed = discord.Embed(description = "SN : " + SN + " -> does not exist.", color=0xeee657)
                    await self.bot.send_message(message.channel, embed = embed)

                
                else:
                    # first attribute : solo, second : flex
                    RANK = self.riot.getRank(SID)
                    if RANK == '-1':
                        embed = discord.Embed(description = "Something error!", color=0xeee657)
                        await self.bot.send_message(message.channel, embed = embed)
                    else:
                        description = "SN : " + SN + "\n" + "Solo : " + RANK[0] + "\n" + "Flex : " + RANK[1]
                        embed = discord.Embed(description = description, color=0xeee657)
                        await self.bot.send_message(message.channel, embed = embed)

        #current game from SN
        if (message.content.startswith('?current') or message.content.startswith('?c')) and message.channel.id == self.channel_id:
            query = message.content
            if message.content.startswith('?current'):
                query = query[8:]
            else:
                query = query[2:]

            if query[0] == " ":
                query = query[1:]

            print(query)
            SN = query
            SID = self.riot.getID(SN)

            if SID == "404":
                embed = discord.Embed(description = "SN : " + SN + " -> does not exist.", color=0xeee657)
                await self.bot.send_message(message.channel, embed = embed)

            else:
                GAME = self.riot.currentGame(SID)


                if GAME == "404":
                    embed = discord.Embed(description = "This Summoner is not in game.", color=0xeee657)
                    await self.bot.send_message(message.channel, embed = embed)


                elif GAME == "OTHER":
                    embed = discord.Embed(description = "This Bot doesn't support this game mode.", color=0xeee657)
                    await self.bot.send_message(message.channel, embed = embed)

                else:#return GAME_MODE, PLAYERS, BANNS, TIME

                    try:#to catch error
                        description = ""

                        embed = discord.Embed(description = GAME['GAME_MODE'], color=0xeee657)
                        await self.bot.send_message(message.channel, embed = embed)

                        for PLAYER in GAME['PLAYERS']:
                            description += PLAYER['summonerName'] + "\n"

                            #get rank info
                            RANK = self.riot.getRank(PLAYER['summonerId'])
                            if RANK == '-1':
                                description += "Something error!" + "\n\n"
                            else:
                                description += "Solo : " + RANK[0] + " " + "Flex : " + RANK[1] + "\n\n"

                        m, s = divmod(GAME['TIME'], 60)

                        description += "Time : " + m + " min" + s " sec" + "\n"

                        embed = discord.Embed(description = description, color=0xeee657)
                        await self.bot.send_message(message.channel, embed = embed)


                    except:
                        print("Something error!")   
                        traceback.print_exc()
