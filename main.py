import discord
import requests
import datetime
import os
import logging

from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_data():
    data = requests.get('https://corona.lmao.ninja/v2/countries/greece?strict=true&query').json()
    cases = data['todayCases']
    deaths = data['todayDeaths']
    critical = data['critical']
    date = datetime.datetime.fromtimestamp(float(1610986013083)/1000.).strftime("%d %b %Y")
    return date, cases, deaths, critical


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    def should_send_data(message):
        text = message.content
        return text.startswith('/krousmata') or text.startswith('/gkrouzmata') or client.user.mentioned_in(message)

    if should_send_data(message):
        date, cases, deaths, critical = get_data()
        await message.channel.send(f'{date}: {cases} κρούσματα | {deaths} θάνατοι | {critical} ΜΕΘ')


if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
