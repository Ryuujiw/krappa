import os
import discord
from dotenv import load_dotenv
import asyncio
import pandas as pd
from datetime import datetime
import pytz
from podium import generate_image

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

client = discord.Client()

@client.event
async def on_ready():
    print('krappa is now online')

@client.event
async def on_message(message):

    if message.content.endswith('who'):
        # get the emote
        emote_to_check = message.content.split()[0].lower()

    if 'emote_to_check' not in vars():
        return

    # init dataframe
    data = pd.DataFrame(columns=['author', 'message', 'reactions', 'time'])
    
    # get 1st day of current month -> today
    timezone = pytz.timezone('Asia/Kuala_Lumpur')
    today = datetime.now(timezone).replace(tzinfo=None)

    async for msg in message.channel.history(before=today, after=today.replace(day=1, hour=0, minute=0, second=0), limit=None):
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
                elif emote.emoji == emote_to_check:
                    # for default emoji
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

    # init embed
    embed = discord.Embed(title= emote_to_check + " of the month", color=0x00ff00)

    for winner in winners:
        embed.add_field(name="Author", value=winner['author'])
        embed.add_field(name="Message", value='[%s](%s)'%(winner['message'],winner['message_url']))
        embed.add_field(name= emote_to_check + "'d", value=winner['reactions'])
        embed.add_field(name="Time", value=winner['time'])
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name = chr(173), value = chr(173))

    file = discord.File(".assets/tmp/winners.png", filename="image.png") if generate_image(winners) == True else None
    embed.set_image(url="attachment://image.png")
        
    await message.channel.send(file=file, embed=embed)

client.run(TOKEN)