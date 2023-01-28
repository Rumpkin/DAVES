import discord,threading,asyncio
from discord.ext import commands
import requests

from enum import Enum
from datetime import datetime

import pytz # timezone



utc = pytz.timezone('US/Pacific')

class SecurityLevel():
    
    def __init__(self, logMessages:bool, notifyParent:bool, blockSender:bool, leaveChat:bool, deleteExpictMessagesSent:bool, lockMessageSending:bool):
        self.logMessages = logMessages
        self.notifyParent = notifyParent
        self.blockSender = blockSender
        self.leaveChat = leaveChat
        self.deleteExpictMessagesSent = deleteExpictMessagesSent
        self.lockMessageSending = lockMessageSending
        

canSendMessages = True

Alert = SecurityLevel(True, True, True, True, True, True)
Slient = SecurityLevel(True, True, False, False, False, False)
Standby = SecurityLevel(False, False, False, False, False, False)
Custom = SecurityLevel(True, False, False, False, True, True)


detectionMode = Custom

bot = commands.Bot(command_prefix='>', self_bot=True)

@bot.event
async def on_connect():
    print("Connected!")

@bot.event
async def on_message(ctx:commands.Context):    
    if (ctx.guild == None):
        if (ctx.author.id == ctx.channel.me.id and not canSendMessages):
            await ctx.delete()
        else:
            if (ctx.content == "balls"):
                await triggerSecurity(ctx)
            if (detectionMode.logMessages):
                print(ctx.content)
                with open('./messageLog.txt', 'a') as fd:
                    fd.write(ctx.author.name + '#' + str(ctx.author.discriminator) + ' : ' + ctx.content + ' : ' + str(utc.localize(datetime.now())) +'\n')

@bot.event
async def on_message_edit(beforeCtx, afterCtx:commands.Context):
    if (afterCtx.guild == None):
        if (afterCtx.author.id == afterCtx.channel.me.id and not canSendMessages):
            await afterCtx.delete()
        else:
            if (afterCtx.content == "dick"):
                await triggerSecurity(afterCtx)
            if (detectionMode.logMessages):
                print(afterCtx.content)
                with open('./messageLog.txt', 'a') as fd:
                    fd.write(afterCtx.author.name + '#' + str(afterCtx.author.discriminator) + ' : ' + afterCtx.content + ' : ' + str(utc.localize(datetime.now())) +'\n')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

async def triggerSecurity(ctx:commands.Context):
    if (detectionMode.notifyParent):
        if (ctx.author.id == ctx.channel.me.id):
            print('your child is a bad person. they said "' + ctx.content + '"')
        else:
            print(ctx.author.name + ' said "' + ctx.content + '" to your child')
    
    if (detectionMode.deleteExpictMessagesSent):
        if (ctx.author.id == ctx.channel.me.id):
            await ctx.delete()
            if (detectionMode.lockMessageSending):
                global canSendMessages
                canSendMessages = False

    if (detectionMode.blockSender):
        block(ctx)

    if (detectionMode.leaveChat):
        closeChannel(ctx)

def block(ctx):
    headers = {"authorization": token, "user-agent": "Mozilla/5.0"}
    json = {"type": 2}
    bloke = requests.put(
        f"https://canary.discord.com/api/v8/users/@me/relationships/{ctx.author.id}",
        headers=headers,
        json=json,
    )

def closeChannel(ctx):
    headers = {"authorization": token, "user-agent": "Mozilla/5.0"}
    close = requests.delete(
        f"https://canary.discord.com/api/v8/channels/{ctx.channel.id}",
        headers=headers
    )

token = 'MzM1MTk3MTMyODc5NDI5NjMy.G3D_4N.G8N8d8Oqz36XRhF25iJA9MTBRdXcPUzex84jEY'
bot.run(token)