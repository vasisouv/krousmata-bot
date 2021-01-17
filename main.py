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


def fetch_cases(endpoint):
    r = requests.get(f'https://covid-19-greece.herokuapp.com/{endpoint}')
    d = r.json()
    cases = d['cases']
    return cases


def get_date_confirmed_and_deaths():
    cases = fetch_cases('all')
    last_known = cases[-1]
    p_last_known = cases[-2]
    confirmed = last_known['confirmed'] - p_last_known['confirmed']
    deaths = last_known['deaths'] - p_last_known['deaths']
    date = datetime.datetime.strptime(last_known['date'], '%Y-%m-%d').strftime("%d %b %Y")
    return date, confirmed, deaths


def get_intensive():
    cases = fetch_cases('intensive-care')
    return cases[-1]['intensive_care']


def get_data():
    date, confirmed, deaths = get_date_confirmed_and_deaths()
    intensive = get_intensive()
    return date, confirmed, deaths, intensive


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
        date, confirmed, deaths, intensive = get_data()
        await message.channel.send(f'{date}: {confirmed} κρούσματα | {deaths} θάνατοι | {intensive} ΜΕΘ')


if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN'))
