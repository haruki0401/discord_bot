import discord
from discord.ext import commands

class Defaultcog:

    def __init__(self, bot, riot):
        self.bot = bot
        self.riot = riot

    # replay "にゃーん"
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
                if (type(args[0]) is int) and (type(args[1]) is int):
                    ans = int(args[0]) + int(args[1])
                    embed = discord.Embed(description = ans, color=0xeee657)
                    await self.bot.say(embed = embed) 
                
                else:
                    embed = discord.Embed(description = "please enter correct parameters!", color=0xeee657)
                    await self.bot.say(embed = embed) 
        
    # delete all msg (admin only)
    @commands.command(pass_context=True)
    async def clean(self, ctx):
        '''delete all msg (Only admin can usethis command)'''
        if ctx.message.channel.id == '536814382705934338'and ctx.message.author.server_permissions.administrator: # admin only command
            clean_flag = True
            while (clean_flag):
                msgs = [msg async for msg in self.bot.logs_from(ctx.message.channel)]
                if len(msgs) > 1: # 1発言以下でdelete_messagesするとエラーになる
                    await self.bot.delete_messages(msgs)
                else:
                    clean_flag = False
                    embed = discord.Embed(description = "deleted all msgs!!", color=0xeee657)
                    await self.bot.say(embed = embed)

    # get rank info
    @commands.command(pass_context=True)
    async def rank(self, ctx, *args):
        '''get League of Legends rank info from SN (e.g. !rank Berry Summer)'''
        if ctx.message.channel.id == '536814382705934338':
            sn = ""
            for str in args:
                sn = sn + " " + str
            
            sn = sn[1:]
            print(sn)                
            
            SID = self.riot.getID(sn)   
            
            if SID == "-1":
                embed = discord.Embed(description = "The Summoner Name you entered does not exist.", color=0xeee657)
                await self.bot.say(embed = embed)

            else:
                # first attribute : solo, second : flex
                RANK = self.riot.getRank(SID)
                if RANK == '-1':
                    embed = discord.Embed(description = "Something error!", color=0xeee657)
                    await self.bot.say(embed = embed)
                else:
                    description = "Solo : " + RANK[0] + "\n" + "Flex : " + RANK[1]
                    embed = discord.Embed(description = description, color=0xeee657)
                    await self.bot.say(embed = embed)