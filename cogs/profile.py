import discord
from discord.ext import commands
import crasync
import aiohttp
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
        if tag is None:
            tag = self.tag
            if tag is None:
                em.description - 'Please add `TAG` to your config.'
                return await ctx.send(embed=em)
        try:
            profile = await self.client.get_profile(tag)
        except:
            em.description = 'Either the API is down or that\'s an invalid tag.'
            return await ctx.send(embed=em)

        clan = await profile.get_clan()

        if clan.name is not None:
            clan_badge = clan.badge_url
            clan_members = str(len(clan.members)) + '/50'

        level = str(profile.level)
        experience = str(profile.experience[0]) + '/' + str(profile.experience[1])
        trophies = str(profile.current_trophies)
        highest_trophies = str(profile.highest_trophies)
        legend_trophies = str(profile.legend_trophies)
        arena = profile.arena.name + ' | Arena ' + str(profile.arena.number)

        em.title = profile.name
        em.description = f'#{tag}'
        em.url = f'http://cr-api.com/profile/{tag}'
        if clan.name is not None:
            em.set_author(name='Profile', icon_url=clan_badge)
            em.add_field(name='Level', value=level)
            em.add_field(name='Experience', value=experience)
            em.add_field(name='Arena', value=arena)

            em.add_field(name='Current Trophies', value=trophies)
            em.add_field(name='Highest Trophies', value=highest_trophies)
            em.add_field(name='Legend Trophies', value=legend_trophies)

            em.add_field(name='Clan Name', value=clan.name)
            em.add_field(name='Clan Tag', value='#' + clan.tag)
            em.add_field(name='Clan Region', value=clan.region)
            em.add_field(name='Clan Members', value=clan_members)
        else:
            em.set_author(name='Profile')
            em.add_field(name='Level', value=level)
            em.add_field(name='Experience', value=experience)
            em.add_field(name='Arena', value=arena)

            em.add_field(name='Current Trophies', value=trophies)
            em.add_field(name='Highest Trophies', value=highest_trophies)
            em.add_field(name='Legend Trophies', value=legend_trophies)

            em.add_field(name='Clan', value='No clan')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Profile(bot))
