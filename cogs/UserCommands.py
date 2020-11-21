import discord, random, aiohttp, time, json
from datetime import datetime, date, time, timedelta
from discord.ext import commands
from discord.ext.commands import has_permissions
from .Settings import *
from .GlobalFunctions import *



# Cog
class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description='Shows that the bot is working', aliases=['test', 'pong'], usage='ping')
    async def ping(self, ctx):
        await successEmbed(ctx,'🏓 Pong', 'NoBot is working!')
    
    
    @commands.command(description='Flips a coin 50/50 chance the coin might land on heads or tails', aliases=['flipacoin'], usage='coinflip')
    async def coinflip(self, ctx):
        flip_num = random.randrange(-1,1)
        if flip_num == 0:
            await successEmbed(ctx, 'The coin landed on...', '**Heads**')
        else:
            await successEmbed(ctx, 'The coin landed on...', '**Tails**')

    @commands.command(description='Rolls a dice with user specified sides', usage='diceroll (number)')
    async def diceroll(self, ctx, message):
        if not message.isdigit():
            await errorEmbed(ctx, 'Argument error', 'Argument must be a digit.')
        if int(message)<1:
            await ctx.send('Number of dice faces must be higher than 0.')
        else:
            dice_number = random.randrange(1, int(message))
            await ctx.send(f'🎲The dice landed on **{dice_number}**')
        
    @commands.command(description='Sends a random hug GIF to a user', usage='hug @user')
    async def hug(self, ctx, member: discord.Member):
        async with aiohttp.ClientSession() as r:
            await ctx.message.delete()
            search = 'anime hug'
            filter_content = 'medium'
            async with r.get(f'https://api.tenor.com/v1/random?q={search}&key={settings["tenor_key"]}&limit=1&contentfilter={filter_content}') as result:
                if result.status == 200:
                    context = await result.text()
                    gif = json.loads(context)
                    if ctx.author.id == member.id:
                        await ctx.send(f'aw you hugged yourself :( \n{gif["results"][0]["url"]}')
                    else:
                        await ctx.send(f'<@{ctx.author.id}> hugged <@{member.id}>\n{gif["results"][0]["url"]}')
                else:
                    await errorEmbed(ctx, 'Error', 'Seems like Tennor forgot to pay the internet bills')
     

           
    # Error handling
    
    @diceroll.error
    async def dice_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await errorEmbed(ctx, 'Missing argument', f'Command Example: `{settings["bot_prefix"]}diceroll {random.randint(1,10)}`')
        
    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await errorEmbed(ctx, 'Missing argument', f'Command Example: `{settings["bot_prefix"]}hug @user`')
                             

def setup(bot):
    bot.add_cog(UserCommands(bot))