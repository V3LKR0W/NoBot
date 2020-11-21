import discord, datetime
from datetime import date

# Global Cog functions

async def errorEmbed(ctx, title, description):
    embed = discord.Embed(
        title = str(title),
        description = str(description),
        color = 0xD21919,
    )
    embed.set_footer(text='NoBot | '+str(date.today().strftime('%m/%d/%y')))
    await ctx.send(embed=embed)
                               
async def successEmbed(ctx, title, description):
    embed = discord.Embed(
        title = str(title),
        description = str(description),
        color = 0x39E01B,
    ) 
    embed.set_footer(text='NoBot | '+str(date.today().strftime('%m/%d/%y'))+' | •'+str(ctx.guild)+' •'+str(ctx.channel.name))
    await ctx.send(embed=embed)
                              
async def returnEmbed(ctx, title, description):
    embed = discord.Embed(
        title = str(title),
        description = str(description),
        color = 0x0835FF,
    )
    embed.set_footer(text='NoBot | '+str(date.today().strftime('%m/%d/%y'))+' | •'+str(ctx.guild)+' •'+str(ctx.channel.name))
    await ctx.send(embed=embed)   
    
async def messageReturnEmbed(member, title, description):
    embed = discord.Embed(
        title = str(title),
        description = str(description),
        color = 0x0835FF,
    )
    embed.set_footer(text='NoBot | '+str(date.today().strftime('%m/%d/%y')))
    await member.send(embed=embed)
    
async def messageErrorEmbed(member, title, description):
    embed = discord.Embed(
        title = str(title),
        description = str(description),
        color = 0xD21919,
    )
    embed.set_footer(text='NoBot | '+str(date.today().strftime('%m/%d/%y')))
    await member.send(embed=embed)  