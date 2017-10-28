import discord
from discord.ext import commands
import crasync
import json
import os


class Profile:

    def __init__(self, bot):
        self.bot = bot
        with open('data/config.json') as f:
            config = json.load(f)
            if 'TAG' not in config:
                tag = None
            else:
                tag = config['TAG']
        self.tag = os.environ.get('TAG') or tag
        self.client = crasync.Client()

    @commands.command()
    async def profile(self, ctx, tag=None):
        '''Fetch a Clash Royale Profile'''
        em = discord.Embed(title='Profile')
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        if tag == None:
            tag = self.tag
            if tag == None:
                em.description - 'Please add `TAG` to your config.'
                return await ctx.send(embed=em)
        try:
            profile = await self.client.get_profile(tag)
        except:
            em.description = 'Either the API is down or that\'s an invalid tag.'
            return await ctx.send(embed=em)

        em.title = profile.name
        em.description = f'#{tag}'
        em.url = f'http://cr-api.com/profile/{tag}'
        try:
            em.set_author(name='Profile', icon_url=profile.clan_badge_url)
        except:
            em.set_author(name='Profile')

        await ctx.send(embed=em)
