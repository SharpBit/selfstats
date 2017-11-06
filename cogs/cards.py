import discord
from discord.ext import commands
import crasync
import aiohttp
import json
import os


class Cards:
    '''Get info about a card'''

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

    @commands.command(aliases=['card', 'ci'])
    async def cardinfo(self, ctx, *, card):
        '''Get the info of a card'''
        aliases = {
            "log": "the log",
            "pump": 'elixir collector',
            'skarmy': 'skeleton army',
            'pekka': 'p.e.k.k.a',
            'mini pekka': 'mini p.e.k.k.a'
        }
        card = card.lower()
        if card in aliases:
            card = aliases[card]

        try:
            color = await ctx.get_dominant_color(ctx.author.avatar_url)
            em = discord.Embed(title=card.title(), color=color)
            em.set_author(name='Card Info', icon_url=ctx.author.avatar_url)
            em.description = card.description
            em.add_field(name='Rarity', value=card.rarity)
            em.add_field(name='Type', value=card.type)
            em.add_field(name='Arena', value='Arena ' + str(card.arena))
            em.add_field(name='Cost', value='{card.elixir} elixir')

            em.set_thumbnail(url='attachment://card.png')
            em.set_footer(name='Selfbot made by SharpBit | Powered by cr-api',
                          icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

            with open(f"data/cards/{card.replace(' ', '-').replace('.','')}.png", 'rb') as c:
                await ctx.send(embed=em, files=[discord.File(c, 'card.png')])
        except KeyError:
            await ctx.send('That\'s not a card.')


def setup(bot):
    bot.add_cog(Cards(bot))
