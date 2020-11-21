import discord, random
from datetime import date
from discord.ext import commands
from discord.ext.commands import has_permissions
from .Settings import *
from .GlobalFunctions import *


# Cog
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description='Removes messages in mass', usage='purge (number)')
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, number):
        try:
            await ctx.channel.purge(limit=int(number))
            await successEmbed(ctx,'Success!', f'Purged `{number}` messages')
        except ValueError:
            await errorEmbed(ctx, 'Value Error', f'You must specify a number of messages you would like to delete')

    @commands.command(description='Bans user from the server', usage='ban @user reason')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        guild = ctx.guild
        author = ctx.message.author.id
        embed = discord.Embed(
            title = 'Server Ban',
            description = f'You have been banned from **{guild}**.',
            color = 0xD21919,
        )
        embed.add_field(
            name = 'Reason:',
            value = str(reason),
            inline = False,
        )
        embed.add_field(
            name = 'Reminder:',
            value = 'Circumvent this ban may result in a global ban in all servers using NoBot and may also result in your discord account getting terminated.',
            inline = False,
        )
        await member.send(embed=embed)
        await ctx.message.delete()
        await successEmbed(ctx,'Successfully Banned',f'{member} was banned for **{reason}**')
        await member.ban(reason=str(reason))

    @commands.command(description='Unbans user from the server', usage='unban user#1234')
    @has_permissions(ban_members=True)
    async def unban(self ,ctx, *, member, reason=None):
        author = ctx.message.author.id
        await ctx.message.delete()
        banned_users = await ctx.guild.bans()
        memeber_name, member_discrim = member.split('#')
        for bans in banned_users:
            user = bans.user
            if (user.name, user.discriminator) == (memeber_name, member_discrim):
                await ctx.guild.unban(user)
                await successEmbed(ctx, 'Successfully unbanned', f'{user.name}#{user.discriminator}')

    @commands.command(description='Kicks user from the server', usage='kick @user reason')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        author = ctx.message.author.id
        guild = ctx.guild
        await ctx.message.delete()
        await ctx.send(f'<@{author}> `{member}` has been kicked for `{reason}`')
        embed = discord.Embed(
            title = 'Server Kicked',
            description = f'You have been kicked from **{guild}**.',
            color = 0xD21919,
        )
        embed.add_field(
            name = 'Reason:',
            value = str(reason),
            inline = False, 
        )
        await member.send(embed=embed)
        await ctx.guild.kick(member) 

    @commands.command(description='Warns a user specific infraction', usage='warn @user reason')
    @has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.User, *, reason):
        author = ctx.message.author.id 
        user_id = user.id
        await ctx.message.delete()
        await errorEmbed(ctx, 'Warned', f'<@{user_id}> you have been warned for **{reason}**')


    @commands.command(description='Shows all active invites on the guild', usage='invites')
    @has_permissions(manage_guild=True)
    async def invites(self, ctx):
        invites = await ctx.guild.invites()
        if not invites:
            await errorEmbed(ctx, 'Error', 'No active invites found')
        else:
            await returnEmbed(ctx, 'List of current active invites', f'\n'.join(str(x) for x in invites))
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await errorEmbed(ctx, 'Missing argument', f'Command Example: `{settings["bot_prefix"]}ban User Reason`')
        elif isinstance(error, commands.MissingPermissions):
            await errorEmbed(ctx, 'Incorrect permissions to perform this command', 'Ban permissions needed to invoke')
        elif discord.Forbidden:
            await errorEmbed(ctx, 'Error', 'Unable to perform action on user')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await errorEmbed(ctx ,'Missing argument', f'Command Example: `{settings["bot_prefix"]}kick User Reason`')
        elif isinstance(error, commands.MissingPermissions):
            await errorEmbed(ctx, 'Incorrect permissions to perform this command', 'Kick permissions needed to invoke')
        elif discord.Forbidden:
            await errorEmbed(ctx, 'Error', 'Unable to perform action on user')

    @unban.error 
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await errorEmbed(ctx, 'Missing argument', f'Command Example: `{settings["bot_prefix"]}unban User`') 
        elif isinstance(error, commands.MissingPermissions):
            await errorEmbed(ctx, 'Incorrect permissions to perform this command', 'Ban permissions needed to invoke')
        elif discord.Forbidden:
            await errorEmbed(ctx, 'Not found', 'Unable to perform action because user was not found')
        
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await errorEmbed(ctx, 'Missing argument', f'Command Example: `{settings["bot_prefix"]}warn User Reason`')
        elif isinstance(error, commands.MissingPermissions):
            await errorEmbed(ctx, 'Incorrect permissions to perform this command', 'Administrator permissions needed to invoke')


    @invites.error
    async def invite_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await errorEmbed(ctx, 'Incorrect permissions to perform this command', 'Manage server permissions needed to invoke')
    
        
def setup(bot):
    bot.add_cog(AdminCommands(bot))