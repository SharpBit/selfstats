import discord
from discord.ext import commands
import crasync
import aiohttp
import random
import json
import os


def random_color(self):
    color = ('#%06x' % random.randint(8, 0xFFFFFF))
    color = int(color[1:], 16)
    color = discord.Color(value=color)
    return color


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

    @commands.command()
    async def card(self, ctx, *, card):
        '''Get the info of a card'''
        arenas = {
            0: 'Training Camp',
            1: 'Goblin Stadium',
            2: 'Bone Pit',
            3: 'Barbarian Bowl',
            4: "P.E.K.K.A's Playhouse",
            5: 'Spell Valley',
            6: "Builder's Workshop",
            7: 'Royal Arena',
            8: 'Frozen Peak',
            9: 'Jungle Arena',
            10: 'Hog Mountain'
        }

        aliases = {
            "log": "the log",
            "pump": 'elixir collector',
            'skarmy': 'skeleton army',
            'pekka': 'p.e.k.k.a',
            'mini pekka': 'mini p.e.k.k.a',
            'xbow': 'x-bow'
        }
        card = card.lower()
        if card in aliases:
            card = aliases[card]

        constants = self.constants
        try:
            found_card = constants.cards[card]
        except KeyError:
            return await ctx.send("That's not a card!")

        color = random_color()
        em = discord.Embed(title=found_card.name, color=color)
        em.set_author(name='Card Info', icon_url=ctx.author.avatar_url)
        em.description = found_card.description
        em.add_field(name='Rarity', value=found_card.rarity)
        em.add_field(name='Type', value=found_card.type)
        em.add_field(name='Arena', value=arenas[found_card.arena])
        em.add_field(name='Cost', value=f'{found_card.elixir} elixir')

        em.set_thumbnail(url='attachment://card.png')
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        with open(f"data/cards/{card.replace(' ', '-').replace('.','')}.png", 'rb') as c:
            await ctx.send(embed=em, files=[discord.File(c, 'card.png')])


def setup(bot):
    bot.add_cog(Cards(bot))
