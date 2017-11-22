import discord
from discord.ext import commands
import textwrap
import random
import crasync
import aiohttp
import psutil
import json
import sys
import os
import re

_mentions_transforms = {
    '@everyone': '@\u200beveryone',
    '@here': '@\u200bhere'
}

_mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

bot = commands.Bot(command_prefix=os.environ.get('PREFIX') or 'cr.', self_bot=True)
process = psutil.Process()
cogs = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
bot.remove_command('help')


path = 'cogs.'
for cog in cogs:
    try:
        bot.load_extension(f'{path}{cog}')
        print(f'Loaded extension: {cog}')
    except Exception as e:
        print(f'LoadError: {cog}\n'
              f'type(e).__name__: {e}')


def random_color():
    color = ('#%06x' % random.randint(8, 0xFFFFFF))
    color = int(color[1:], 16)
    color = discord.Color(value=color)
    return color


@property
def tag():
    '''Returns your Clash Royale tag'''
    with open('data/config.json') as f:
        config = json.load(f)
        if config.get('TAG') == "your_tag_here":
            if not os.environ.get('TAG'):
                run_wizard()
        else:
            tag = config.get('TAG').strip('#').replace('O', '0')
    return os.environ.get('TAG') or tag


async def on_ready():
    '''Bot startup, sets uptime'''
    print(textwrap.dedent(f'''
    Use this at your own risk,
    don't do anything stupid,
    and when you get flagged,
    don't blame it at me.
    ---------------
    Client is ready!
    ---------------
    Author: SharpBit#1510
    ---------------
    Logged in as: {bot.user}
    User ID: {bot.user.id}
    ---------------
    Current Version: 1.0.0
    ---------------
    '''))

    await bot.change_presence(status=discord.Status.invisible, afk=True)


async def on_message(message):
    '''Responds only to yourself'''
    if message.author.id != bot.user.id:
        return
    await bot.process_commands(message)


def get_server(id):
    return discord.utils.get(bot.guilds, id=id)


@bot.command()
async def ping(ctx):
    '''Pong! Returns your latency'''
    em = discord.Embed()
    em.title = 'Pong! Latency:'
    em.description = f'{bot.ws.latency * 1000:.4f} ms'
    em.color = random_color()
    await ctx.send(embed=em)


@bot.command(aliases=['bot', 'info'])
async def about(ctx):
    '''See information about the selfbot and latest changes.'''

    embed = discord.Embed()
    embed.color = random_color()

    embed.set_author(name='selfstats.py', icon_url=ctx.author.avatar_url)

    total_online = len({m.id for m in bot.get_all_members()
                        if m.status is discord.Status.online})
    total_unique = len(bot.users)

    voice_channels = []
    text_channels = []
    for guild in bot.guilds:
        voice_channels.extend(guild.voice_channels)
        text_channels.extend(guild.text_channels)

    text = len(text_channels)
    voice = len(voice_channels)
    dm = len(bot.private_channels)

    github = '[Click Here](https://github.com/SharpBit/selfstats/)'
    server = '[Click Here](https://discord.gg/9NjbQCd)'

    embed.add_field(name='Author', value='SharpBit#1510')
    embed.add_field(name='Guilds', value=len(bot.guilds))
    embed.add_field(name='Members', value=f'{total_unique} total\n{total_online} online')
    embed.add_field(name='Channels', value=f'{text} text\n{voice} voice\n{dm} direct')
    memory_usage = bot.process.memory_full_info().uss / 1024**2
    cpu_usage = bot.process.cpu_percent() / psutil.cpu_count()
    embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')
    embed.add_field(name='GitHub', value=github)
    embed.add_field(name='Discord', value=server)
    embed.set_footer(text=f'Powered by discord.py {discord.__version__}')
    await ctx.send(embed=embed)


if __name__ == '__main__':
    if not os.environ.get('TOKEN'):
        print('Add token to your config vars.')
    bot.run(os.environ.get('TOKEN').strip('\"'), bot=False, reconnect=True)
