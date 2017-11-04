import discord
from discord.ext import commands
import crasync
import aiohttp
import json
import os


class Clan:
    '''Get info about a clan'''

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
    async def clan(self, ctx, clan_tag=None):
        em = discord.Embed(title='Clan Info')
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)

        if clan_tag is None:
            tag = self.tag
            if tag is None:
                em.description - 'Please add `TAG` to your config.'
                return await ctx.send(embed=em)
            try:
                profile = await self.client.get_profile(tag)
            except:
                em.description = 'Either the API is down or your tag is an invalid player tag.'
                return await ctx.send(embed=em)
        else:
            clan = await self.client.get_clan(clan_tag)

        try:
            clan = await profile.get_clan()
        except ValueError:
            em.description = 'You are not in a clan'
            return await ctx.send(embed=em)
        except Exception as e:
            return await ctx.send(f'```{e}```')

        if clan.rank == 0:
            rank = 'Unranked'
        else:
            rank = str(clan.rank)

        em.title = clan.name + '(#' + clan.tag + ')'
        em.set_author(name='Clan Info', icon_url=ctx.author.avatar_url)
        em.description = clan.description

        em.add_field(name='Score', value=str(clan.score))
        em.add_field(name='Required Trophies', value=str(clan.required_trophies))
        em.add_field(name='Donations', value=str(clan.donations))
        em.add_field(name='Region', value=clan.region)
        em.add_field(name='Global Rank', value=rank)
        em.add_field(name='Type', value=clan.type_name)

        em.set_thumbnail(url=clan.badge_url)
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Clan(bot))
