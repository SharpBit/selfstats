import discord
from discord.ext import commands
from ext.context import CustomContext
from ext.formatter import EmbedHelp
from collections import defaultdict
from ext import embedtobox
import textwrap
import crasync
import asyncio
import aiohttp
import psutil
import datetime
import time
import json
import sys
import os
import re
import io


class Selfbot(commands.Bot):
    '''Custom Client for selfstats.py - Made by Jason#1510'''
    _mentions_transforms = {
        '@everyone': '@\u200beveryone',
        '@here': '@\u200bhere'
    }

    _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

    def __init__(self, **attrs):
        super().__init__(command_prefix=self.get_pre, self_bot=True)
        self.formatter = EmbedHelp()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.process = psutil.Process()
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.last_message = None
        self.messages_sent = 0
        self.commands_used = defaultdict(int)
        self._add_commands()
        self.load_extensions()

    def _add_commands(self):
        '''Adds commands automatically'''
        for attr in dir(self):
            cmd = getattr(self, attr)
            if isinstance(cmd, commands.Command):
                self.add_command(cmd)

    def load_extensions(self, cogs=None, path='cogs.'):
        '''Loads the default set of extensions or a separate one if given'''
        for extension in cogs or self._extensions:
            try:
                self.load_extension(f'{path}{extension}')
                print(f'Loaded extension: {extension}')
            except Exception as e:
                print(f'LoadError: {extension}\n'
                      f'type(e).__name__: {e}')

    @property
    def token(self):
        '''Returns your token'''
        try:
            with open('data/config.json') as f:
                config = json.load(f)
                if config.get('TOKEN') == "your_token_here":
                    if not os.environ.get('TOKEN'):
                        self.run_wizard()
                    else:
                        token = config.get('TOKEN').strip('\"')
        except FileNotFoundError:
            token = None
        return os.environ.get('TOKEN') or token

    @property
    def tag(self):
        '''Returns your Clash Royale tag'''
        with open('data/config.json') as f:
            config = json.load(f)
            if config.get('TAG') == "your_tag_here":
                if not os.environ.get('TAG'):
                    self.run_wizard()
            else:
                tag = config.get('TAG').strip('#')
        return os.environ.get('TAG') or tag

    @staticmethod
    async def get_pre(bot, message):
        '''Returns the prefix'''
        with open('data/config.json') as f:
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 'cr.'

    @staticmethod
    def run_wizard():
        '''Wizard for first start'''
        print('------------------------------------------')
        token = input('Enter your token:\n> ')
        print('------------------------------------------')
        prefix = input('Enter a prefix for your Clash Royale Stats selfbot:\n> ')
        tag = input('Enter your Clash Royale tag:\n> ')
        data = {
            "TOKEN": token,
            "PREFIX": prefix,
            "TAG": tag
        }
        with open('data/config.json', 'w') as f:
            f.write(json.dumps(data, indent=4))
        print('------------------------------------------')
        print('Restarting...')
        print('------------------------------------------')
        os.execv(sys.executable, ['python'] + sys.argv)

    @classmethod
    def init(bot, token=None):
        '''Starts the actual selfbot'''
        selfbot = bot()
        safe_token = token or selfbot.token.strip('\"')
        try:
            selfbot.run(safe_token, bot=False, reconnect=True)
        except Exception as e:
            print(e)

    async def on_connect(self):
        print('---------------\n'
              'selfstats.py connected!')

    async def on_ready(self):
        '''Bot startup, sets uptime'''
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print(textwrap.dedent(f'''
        Use this at your own risk,
        don't do anything stupid,
        and when you get banned,
        don't blame it at me.
        ---------------
        Client is ready!
        ---------------
        Author: Jason#1510
        ---------------
        Logged in as: {self.user}
        User ID: {self.user.id}
        ---------------
        Current Version: 1.0.0
        ---------------
        '''))

        await self.change_presence(status=discord.Status.invisible, afk=True)

    async def on_command(self, ctx):
        cmd = ctx.command.qualified_name.replace(' ', '_')
        self.commands_used[cmd] += 1

    async def process_commands(self, message):
        '''Utilizes the CustomContext subc;ass of discord.Content'''
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message):
        '''Responds only to yourself'''
        if message.author.id != self.user.id:
            return
        self.messages_sent += 1
        self.last_message = time.time()
        await self.process_commands(message)

    def get_server(self, id):
        return discord.utils.get(self.guilds, id=id)

    @commands.command()
    async def ping(self, ctx):
        '''Pong! Returns your latency'''
        em = discord.Embed()
        em.title = 'Pong! Latency:'
        em.description = f'{self.ws.latency * 1000:.4f} ms'
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(em)
            for page in em_list:
                await ctx.send(page)

    @commands.command(aliases=['bot', 'info'])
    async def about(self, ctx):
        '''See information about the selfbot and latest changes.'''

        embed = discord.Embed()
        embed.color = await ctx.get_dominant_color(ctx.author.avatar_url)

        embed.set_author(name='selfstats.py', icon_url=ctx.author.avatar_url)

        total_online = len({m.id for m in self.get_all_members()
                            if m.status is discord.Status.online})
        total_unique = len(self.users)

        voice_channels = []
        text_channels = []
        for guild in self.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)
        dm = len(self.private_channels)

        now = datetime.datetime.utcnow()
        delta = now - self.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt
        uptime = fmt.format(d=days, h=hours, m=minutes, s=seconds)

        github = '[Click Here](https://github.com/SharpBit/selfstats/)'
        server = '[Click Here](https://discord.gg/9NjbQCd)'

        embed.add_field(name='Author', value='Jason#1510')
        embed.add_field(name='Uptime', value=uptime)
        embed.add_field(name='Guilds', value=len(self.guilds))
        embed.add_field(name='Members', value=f'{total_unique} total\n{total_online} online')
        embed.add_field(name='Channels', value=f'{text} text\n{voice} voice\n{dm} direct')
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')
        embed.add_field(name='GitHub', value=github)
        embed.add_field(name='Discord', value=server)
        embed.set_footer(text=f'Powered by discord.py {discord.__version__}')
        await ctx.send(embed=embed)


if __name__ == '__main__':
    Selfbot.init()
