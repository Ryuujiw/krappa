import os
import discord
import re
from dotenv import load_dotenv
import asyncio
import pandas as pd
import datetime
from PIL import Image
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

client = discord.Client()

@client.event
async def on_ready():
    print('krappa is now online')

@client.event
async def on_message(message):

    emote_to_check = ''

    if message.content.endswith('who'):
        # get the emote
        emote_to_check = message.content.split()[0].lower()

    if emote_to_check == '':
        return

    # init dataframe
    data = pd.DataFrame(columns=['author', 'message', 'reactions', 'time'])
    
    # get 1st day of current month -> today
    today = datetime.datetime.today()
    start_of_the_month = datetime.datetime.today().replace(day=1)
    async for msg in message.channel.history(before=today, after=start_of_the_month, limit=None):
        if msg.author != client.user:
            # skip message if has no reactions
            if len(msg.reactions) == 0:
                continue
            for emote in msg.reactions:
                if hasattr(emote.emoji, 'name') and emote.emoji.name.lower() == emote_to_check:
                    data = data.append({'author': msg.author.name,
                    'message': msg.content,
                    'message_url': msg.jump_url,
                    'reactions' : emote.count,
                    'time': msg.created_at,
                    'avatar_url': msg.author.avatar_url},
                    ignore_index=True)

    # find most krappa
    krappa = data['reactions']
    nominees = data.loc[krappa == krappa.max()]

    # store winners into a csv
    winners = nominees.to_dict('records')

    # init winners' podium
    podium = Image.open("tmp/podium.png")
    size = (80,80)        

    # init embed
    embed = discord.Embed(title= emote_to_check + " of the month", color=0x00ff00)

    for index, winner in enumerate(winners):
        embed.add_field(name="Author", value=winner['author'])
        embed.add_field(name="Message", value='[%s](%s)'%(winner['message'],winner['message_url']))
        embed.add_field(name= emote_to_check + "'d", value=winner['reactions'])
        embed.add_field(name="Time", value=winner['time'])
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name = chr(173), value = chr(173))

        # create winners' podium
        winner = Image.open(requests.get(winner['avatar_url'], stream=True).raw)
        resized_avatar = winner.resize(size)
        # first, second and runner-up
        podium.paste(resized_avatar,(375,40))
        podium.paste(resized_avatar,(120,110))  if index == 1 else None
        podium.paste(resized_avatar,(605,50))   if index == 2 else None
        podium.save('tmp/winners.png')

    file = discord.File("tmp/winners.png", filename="image.png") if len(winners) > 0 else None
    embed.set_image(url="attachment://image.png")
        
    await message.channel.send(file=file, embed=embed)

client.run(TOKEN)