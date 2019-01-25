import discord
from discord.ext import commands

class Defaultcog(commands.Bot):


    def __init__(self, bot, riot):
        self.bot = bot
        self.riot = riot




    async def on_ready(self):
        print("-----")
        print('logged in')
        print("-----")



    # reply "にゃーん"
    @commands.command(pass_context=True)
    async def nyan(self,ctx):
        '''just say nyan~!!''' 
        if ctx.message.channel.id == '536814382705934338':
            embed = discord.Embed(description = "にゃーん＞＜", color=0xeee657)
            await self.bot.say(embed = embed)

    # add
    @commands.command(pass_context=True)
    async def add(self, ctx, *args):
        '''additon of 2 numbers (e.g. !add X Y)'''
        if ctx.message.channel.id == '536814382705934338':
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
        if ctx.message.channel.id == '536814382705934338'and ctx.message.author.server_permissions.administrator: # admin only command
            
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
                        
    #get rank info
    async def on_message(self, message):
        if (message.content.startswith('/rank') or message.content.startswith('/r')) and message.channel.id == '536814382705934338':
            query = message.content
            if message.content.startswith('/rank'):
                query = query[5:]
            else:
                query = query[2:]

            if query[0] == " ":
                query = query[1:]

            #print(query)

            SNs = query.split('\n')
            #print(len(SNs))

            for SN in SNs:
                #print(SN)
                SID = self.riot.getID(SN)   
                
                if SID == "-1":
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
