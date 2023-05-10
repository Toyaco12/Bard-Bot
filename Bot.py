import os
import discord
import pytz
import requests
from datetime import datetime
import aiohttp
from dotenv import load_dotenv
import os
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

async def get_timezone(location):
    geolocator = Nominatim(user_agent="discord_bot")
    try:
        geolocation = geolocator.geocode(location)
        if geolocation:
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=geolocation.longitude, lat=geolocation.latitude)
            return timezone
        else:
            return None
    except Exception as e:
        print(e)
        return None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$time'):
        location = message.content.split(' ')[1]
        timezone = await get_timezone(location)
        if timezone:
            now = datetime.now(pytz.timezone(timezone))
            formatted_time = now.strftime('%Hh%M')
            await message.channel.send(f'The current time in {location} is {formatted_time}')
        else:
            await message.channel.send('Invalid location. Please try again.')

client.run(TOKEN)
