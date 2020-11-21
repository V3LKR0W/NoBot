import discord, random
from datetime import date
from discord.ext import commands
from discord.ext.commands import has_permissions
from .Settings import *
from .GlobalFunctions import *


class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def reloadcog(self, ctx, cog: str):
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            await successEmbed(ctx, 'Unloaded Cog', f'`{cog}`')
            self.bot.load_extension(f'cogs.{cog}')
            await successEmbed(ctx, 'Reloaded Cog', f'`{cog}`')
        except Exception as err:
            await errorEmbed(ctx, '[Error]', f'`{err}`')
    
    @commands.command()
    @commands.is_owner()
    async def disablecog(self, ctx, cog: str):
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            await successEmbed(ctx, 'Unloaded Cog', f'`{cog}`')
        except Exception as err:
            await errorEmbed(ctx, 'Could not unload cog', f'[Error]: `{err}`')

    @commands.command()
    @commands.is_owner()
    async def loadcog(self, ctx, cog: str):
        try:
            self.bot.load_extension(f'cogs.{cog}')
            await successEmbed(ctx, 'Loaded Cog', f'`{cog}`')
        except Exception as err:
            await errorEmbed(ctx, 'Could not loaded', f'[Error]: `{err}`')
        
def setup(bot):
    bot.add_cog(DeveloperCommands(bot))