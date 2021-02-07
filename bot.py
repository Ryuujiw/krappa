import os
import discord
import re
from dotenv import load_dotenv
import asyncio
import pandas as pd
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

client = discord.Client()

@client.event
async def on_ready():
    print('krappa is now online')

@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith('krappa who'):
        return

    # init dataframe
    data = pd.DataFrame(columns=['author', 'reactions', 'time'])
    
    # get 1st day of current month -> today
    today = datetime.datetime.today()
    start_of_the_month = datetime.datetime.today().replace(day=1)

    async for msg in message.channel.history(before=today, after=start_of_the_month):
        if msg.author != client.user:
            # skip message if has no reactions
            if len(msg.reactions) == 0:
                continue
            for emote in msg.reactions:
                if not hasattr(emote.emoji, 'name') or not emote.emoji.name == 'Krappa':
                    continue

                data = data.append({'author': msg.author.name,
                                    'message': msg.content,
                                    'reactions' : emote.count,
                                    'time': msg.created_at},
                                    ignore_index=True)

    # find most krappa
    krappa = data['reactions']
    nominees = data.loc[krappa == krappa.max()]

    # store winners into a csv
    winners = nominees.to_dict('records')

    # init embed
    embed = discord.Embed(title="Krappa of the month", color=0x00ff00)
    embed.set_thumbnail(url="https://cdn.betterttv.net/emote/58cd3345994bb43c8d300b82/3x")

    for winner in winners:
        embed.add_field(name="Author", value=winner['author'])
        embed.add_field(name="Message", value=winner['message'])
        embed.add_field(name="Krappa'd", value=winner['reactions'])
        embed.add_field(name="Time", value=winner['time'])
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name = chr(173), value = chr(173))

    await message.channel.send(embed=embed)

client.run(TOKEN)