
import discord
from discord.ext import commands
import asyncio
from colorthief import ColorThief
from urllib.parse import urlparse
import json
import io
import os


class CustomContext(commands.Context):
    '''Custom Context class to provide utility.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        '''Returns the bot's aiohttp client session'''
        return self.bot.session

    def delete(self):
        '''shortcut'''
        return self.message.delete()

    async def confirm(self, msg):
        '''Small helper for confirmation messages.'''
        await self.send(msg or '*Are you sure you want to proceed?* `(Y/N)`')
        resp = self.bot.wait_for('message', check=lambda m: m == ctx.author)
        falsy = ['n', 'no', 'false', '0', 'fuck off', 'f']
        if resp.content.lower().strip() in falsy:
            return False
        else:
            return True

    async def send_cmd_help(self):
        '''Sends command help'''
        if self.invoked_subcommand:
            pages = self.formatter.format_help_for(self, self.invoked_subcommand)
            for page in pages:
                await self.send_message(self.message.channel, page)
        else:
            pages = self.formatter.format_help_for(self, self.command)
            for page in pages:
                await self.send_message(self.message.channel, page)

    @staticmethod
    def is_valid_image_url(url):
        '''Checks if a url leads to an image.'''
        types = ['.png', '.jpg', '.gif', '.bmp', '.webp']
        parsed = urlparse(url)
        if any(parsed.path.endswith(i) for i in types):
            return url.replace(parsed.query, 'size=128')

    async def success(self, ctx, msg=None, delete=False):
        if delete:
            await ctx.message.delete()
        if msg:
            await self.send(msg)
        else:
            await self.message.add_reaction('✅')

    async def failure(self, msg=None):
        if msg:
            await self.send(msg)
        else:
            await self.message.add_reaction('⁉')

    def load_json(self, path=None):
        with open(path or 'data/config.json') as f:
            return json.load(f)

    def save_json(self, data, path=None):
        with open(path or 'data/config.json', 'w') as f:
            f.write(json.dumps(data, indent=4))

    def save_tag(self, tag):
        data = self.load_json()
        data['TAG'] = tag
        self.save_json(data)

    def get_tag(self):
        data = self.load_json()
        tag = data['TAG']
        return tag

    @staticmethod
    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))
