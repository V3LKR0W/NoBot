from discord.utils import get
from discord.ext import commands
from discord.ext.commands import has_permissions
from collections.abc import Sequence
from datetime import date
import discord, os, time, uuid, asyncio, aiostream, requests, json, random, aiohttp
from keys import *



settings={
    'bot_prefix': '!!',
    
    'default_channel_name': 'nobot-verify',
    
    'channel_message': 'To make sure you are human please verify yourself with NoBot. To verify yourself please **react with the green checkbox (✅) in this channel.**',

    'role_unverified': 'NoBot | Un-Verified',
    
    'role_verified': 'NoBot | Verified',
    
    'role_existing': 'NoBot | Pre-Existing User',
    
    'frontend_url': 'https://crying.world/', 
    
    'backend_url': 'https://backend.crying.world/', 
    
    'token_expire': 480, # 300 sec = 5 minutes / 8 minutes = 480 seconds / 600 seconds = 10 minutes 

}



bot = commands.Bot(command_prefix=settings['bot_prefix'])


@bot.event
async def on_ready():
    print('Bot started @ '+ str(datetime.datetime.today()))
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'For {settings["bot_prefix"]}help'))
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):
            if files=='Settings.py' or files=='GlobalFunctions.py':
                continue
            else:
                try:
                    bot.load_extension(f'cogs.{files[:-3]}')
                    print(f'[Loaded]: {files}')
                except Exception as err:
                    print(f'[Error]: {files} \n {err}')
@bot.event
async def on_guild_join(guild):
    
    await guild.create_text_channel(settings['default_channel_name']) #create text channel
    
    server = get(guild.channels, name=settings['default_channel_name'], type=discord.ChannelType.text) #getting channel
    
    msg = await server.send(settings['channel_message']) #sending default message with instructions
    
    reaction = await msg.add_reaction(emoji='✅')
    
    payload = await addGuildChannelMessage(guild.id, server.id, msg.id)
    
    perms_unverified = discord.Permissions(send_messages=False, read_messages=True, read_message_history=True) #discord role permission for non-verified users
    
    old_default = guild.default_role
    
    await old_default.edit(permissions=discord.Permissions(send_messages=False, read_message_history=False, read_messages=False, connect=False))
    
    perms_verified = discord.Permissions(send_messages=True, read_messages=True, stream=True, embed_links=True, use_external_emojis=True, read_message_history=True, create_instant_invite=True, connect=True, speak=True, change_nickname=True,) #discord role permissions for verified users
    
    role_notverified = await server.guild.create_role(name=settings['role_unverified'], permissions=perms_unverified) #creating the not verified role
    
    role_existinguser= await server.guild.create_role(name=settings['role_verified'], permissions=perms_verified) #creating an existing user role (verified permsissons)
    
    role_verified = await server.guild.create_role(name=settings['role_existing'], permissions=perms_verified) #creating the verified role
    
    await server.set_permissions(role_notverified, read_messages=True) #setting NoBot-Verify channel permissions.
    
    await server.set_permissions(role_existinguser, read_messages=False, send_messages=False, read_message_history=False) #setting NoBot-Verify channel permissions.
    
    await server.set_permissions(role_verified, read_messages=False, send_messages=False, read_message_history=False) #setting NoBot-Verify channel permissions.
    
    embed = discord.Embed(
        title='Thank you for using NoBot!',
        description=f'''NoBot is a free discord bot that stop's most automation, raid and spam bots from entering your server!\n
                    What's even better is we set it all up for you! In your server you should see a channel called `{settings['default_channel_name']}`.\n
                    Inside that channel you should also see a message that includes a "✅" reaction attached to that message.\n 
                    Dont worry about all the members that are already in your server! They have been given a pre-existing user role in the server so they will not need to verify themselves.\n 
                    ''',
        color=0x1aff00,
    )
    embed.add_field(
        name='Found a bug?',
        value=settings['frontend_url']+'report'+'\n',
        inline=False,
    )
    embed.add_field(
        name='Support Development',
        value=settings['frontend_url']+'report'+'\n',
        inline=False,
    )
    
    await guild.owner.send(embed=embed)
    
    for member in guild.members:
        if member == bot.user:
            pass
        else:
            role = discord.utils.get(member.guild.roles, name=settings['role_existing'])
            await member.add_roles(role)


#Functions
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

# Bot Events
@bot.event
async def on_member_join(member):
    async with aiohttp.ClientSession() as session:
        async with session.get(settings['backend_url']+f'/ban-check/{member.id}') as check_back_raw:
            raw = await check_back_raw.text()
            results_json = json.loads(raw)
            try:
                if results_json['status'] == 'Not banned':
                    if member.bot:
                        verified = discord.utils.get(member.guild.roles, name=settings['role_verified'])
                        await member.add_roles(verified)
                    else:
                        un_verified = discord.utils.get(member.guild.roles, name=settings['role_unverified'])
                        await member.add_roles(un_verified)
                        for get_channel in member.guild.channels:
                            if str(get_channel) == str(settings['default_channel_name']):
                                verify_channel = get_channel.id
                                await messageReturnEmbed(member, 'This server uses NoBot user verification', f'Please go to <#{verify_channel}> to access user permissions in **{member.guild}**')
                            else:
                                pass
            except KeyError:
                    await messageErrorEmbed(member, 'You have been banned from all servers using NoBot', f'Reason: **{results_json["reason"]}**')
                    await member.guild.kick(member,reason=results_json['reason'])
    
@bot.event
async def on_member_remove(member):
    guild_id = str(member.guild.id) 
    member_id = str(member.id)

@bot.event
async def on_guild_remove(guild):
    guild_id = guild.id
    await onBotLeave(str(guild_id))


@bot.event
async def on_raw_reaction_add(payload):  
    try:
        if payload.member.bot:
            return
    except AttributeError:
        pass
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id) 
    guild_id = payload.guild_id
    message_id = payload.message_id
    user = payload.member
    user_id = payload.user_id
    
    db = client['bot']
    
    guild_collection = db['guild_Collection'] #guild Collection
    
    dm_collection = db['dm_Collection'] #direct message Collection
    
    token_collection = db['tokens'] #UUID token Collection
    
    user_collection = db['all_users'] #all records Collection 
    
    guild_results = guild_collection.find({'message_id': str(message_id)})
    
    async for result in guild_results:
        databaseid = result['message_id']
        if str(message_id) == str(databaseid):
            if payload.emoji.name == '✅':
                backend = requests.get(settings['backend_url']) 
                if backend.status_code == 200: 
                    token = uuid.uuid4()
                    
                    embed = discord.Embed(
                                        title='Verification:',
                                        description=f'To verify you are not a robot in **{guild}**',
                                        color = 0x343aeb,
                                        )
                    
                    embed.add_field(
                                    name='Link 🔗:',
                                    value=str(settings['frontend_url']+f'verify/{token}'),
                                    inline=False,
                    )
                    
                    embed.add_field(
                        name='Instructions 📃:',
                        value=f'Once verified on the website, please click the (☑) under this message.',
                        inline=False,
                    )
                    
                    message = await user.send(embed=embed)
                    
                    await addDirectMessage(message.id)
                    
                    await message.add_reaction(emoji='☑')
                    
                    await addToken(token, guild, guild_id, user, user_id)
                    await asyncio.sleep(settings['token_expire'])
                    await messageErrorEmbed(user, 'Token expired!',f'Your token expired after {settings["token_expire"]} seconds of being active, please regenerate another token by going back to the server.')
                    await removeToken(str(token))
                    
                else:
                    embed = discord.Embed(
                        title='Error:',
                        color=0xfc0335,
                        description=f'Well this is awkward! Our service is most-likly down if you see this. If this persists for longer than 15 minutes please report it here:'+ settings['frontend_url'] +'report-bug',
                    )
                    message = await user.send(embed=embed)
    dm_results = dm_collection.find({'message_id': str(message_id)})
    
    
    
    
    async for r in dm_results:
        token_results = token_collection.find({'user_id': str(user_id)})
        user_name = bot.get_user(user_id)
        db_messageid = r['message_id']
        if str(message_id) == str(db_messageid):
            if payload.emoji.name == '☑':
                if payload.user_id == 738360037310726254:
                    pass
                else:    
                    async for r in token_results:
                        token = r['token']
                        guild_id = r['guild_id']
                        guild_name = r['guild']
                        user_id = r['user_id']
                        
                        check_back_raw = requests.get(settings['backend_url']+f'check?token={token}')
                        check_back = json.loads(check_back_raw.text)
                        print(check_back['verified'])
                        
                    if check_back['verified'] == 'True':
                        embed = discord.Embed(
                            title='Success!',
                            description=f'You now are verified as a human in **{guild_name}**',
                            color=0x34cf46,
                        )
                        
                        await user_name.send(embed=embed)
                        
                        channel = await bot.fetch_channel(int(payload.channel_id))
                        message = await channel.fetch_message(int(db_messageid))
                        await message.delete()
                        
                        guild = await bot.fetch_guild(int(guild_id))
                        
                        user = await guild.fetch_member(int(user_id))
                        
                        try:
                            un_verified = discord.utils.get(guild.roles, name=settings['role_unverified'])
                            await user.remove_roles(un_verified)
                        
                            verified = discord.utils.get(guild.roles, name=settings['role_verified'])
                            await user.add_roles(verified)
                        except AttributeError:
                            pass
                        
                        await removeDirectMessage(str(message_id))
                        
                        await removeToken(str(token))
                            
                    if check_back['verified'] != 'True':
                        embed_message = discord.Embed(
                            title='Oh noes! Look\'s like something went wrong!',
                            description=f'Our records show that your token was never verified, or it has expired after {settings["token_expire"]} seconds. please try again.',
                            color=0xD21919,
                        )
                        
                        footer = embed_message.set_footer(
                           text=''
                        )
                        
                        error_message = await user_name.send(embed=embed_message)
                      
#Commands
bot.remove_command('help')

@bot.command(description='Shows all bot commands.', usage='help')
async def help(ctx):
    embed = discord.Embed(
        title='Command List',
        color=0xD21919,
    )
    for commands in bot.commands:
        embed.add_field(
            name=str(commands),
            value=f'Description: {commands.description}.\n Usage: `{settings["bot_prefix"]}{commands.usage}`',
            inline=False,
        )
    await ctx.send(embed=embed)

#Bot run
bot.run(discordkey)
