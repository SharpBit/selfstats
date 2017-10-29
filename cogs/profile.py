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

        try:
            clan_name = profile.clan.name
            clan_badge = profile.clan_badge_url
            clan_region = profile.clan.region
            clan_members = str(len(profile.clan.members)) + '/50'
        except:
            pass

        name = profile.name
        level = str(profile.level)
        experience = str(profile.experience[0]) + '/' + str(profile.experience[1])
        trophies = str(profile.current_trophies)
        highest_trophs = str(profile.highest_trophies)
        legend_trophies = str(profile.legend_trophies)
        arena = profile.arena.name + ', Arena ' + str(profile.arena.number)

        em.title = profile.name
        em.description = f'#{tag}'
        em.url = f'http://cr-api.com/profile/{tag}'
        try:
            em.set_author(name='Profile', icon_url=clan_badge)
            em.add_field(name='Player Name', value=name)
            em.add_field(name='Level', value=level + '(' + experience + ')')
            em.add_field(name='Trophies', value='Current: ' + trophies +
                         '\nHighest: ' + highest_trophs + '\nLegend: ' + legend_trophies)
            em.add_field(name='Arena', value=arena)
            em.add_field(name='Clan', value='Name: ' + clan_name + '\nRegion: ' +
                         clan_region + '\nMembers: ' + clan_members)
        except:
            em.set_author(name='Profile')
            em.add_field(name='Player Name', value=name)
            em.add_field(name='Level', value=level + '(' + experience + ')')
            em.add_field(name='Trophies', value='Current: ' + trophies +
                         '\nHighest: ' + highest_trophs + '\nLegend: ' + legend_trophies)
            em.add_field(name='Arena', value=arena)
            em.add_field(name='Clan', value='No clan')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Profile(bot))
