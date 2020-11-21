import pymongo, datetime
import asyncio
import motor.motor_asyncio
from pymongo import MongoClient

discordkey = ''

client = motor.motor_asyncio.AsyncIOMotorClient('')


async def addGuildChannelMessage(guild_id, channel_id, message_id):
    db = client['bot']
    collection = db['guild_Collection']
    
    payload={
    
    'guild_id':str(guild_id),
    'channel_id':str(channel_id),
    'message_id':str(message_id),
    }
    
    collection.insert_one(payload)
    print('added guild entity to database with the guild_id = '+str(guild_id))
    
async def addDirectMessage(message_id):
    db = client['bot']
    collection = db['dm_Collection']
    payload={
        'message_id':str(message_id),
    }
    collection.insert_one(payload)
    print('added message entity with the message_id = '+str(message_id))
    
async def removeDirectMessage(message_id):
    db = client['bot']
    collection = db['dm_Collection']
    collection.delete_one({'message_id':str(message_id)})
    print('deleted message entity with the message_id = '+str(message_id))
    
async def removeToken(token):   
    db = client['bot']
    collection = db['tokens']
    collection.delete_one({'token': str(token)})
    print('deleted token entity = '+str(token))
    
async def addToken(token, guild, guild_id, user, user_id):
    db = client['bot']
    collection = db['tokens']
    payload={
        'token':str(token),
        'guild':str(guild),
        'guild_id':str(guild_id),
        'user':str(user),
        'user_id':str(user_id),
        'verified':'False',
    }
    collection.insert_one(payload)
    print('added token entity with the token = '+str(token))


async def onBotLeave(guild_id):
    db = client['bot']
    collection = db['guild_Collection']
    collection.delete_one({'guild_id':str(guild_id)})
    print('deleted guild entity with the guild_id = '+ str(guild_id))