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

        if profile.global_rank is not None:
            global_rank = str(profile.global_rank)
        else:
            global_rank = 'N/A'

        level = str(profile.level)
        experience = str(profile.experience[0]) + '/' + str(profile.experience[1])
        trophies = str(profile.current_trophies)
        highest_trophies = str(profile.highest_trophies)
        legend_trophies = str(profile.legend_trophies)
        arena = profile.arena.name + ' | Arena ' + str(profile.arena.number)
        donations = str(profile.total_donations)
        win_decimal = f'{profile.wins / (profile.wins + profile.losses):.3f}'
        win_percent = win_decimal + '%'
        record = str(profile.wins) + '-' + str(profile.draws) + '-' + str(profile.losses)

        em.title = profile.name
        em.description = f'#{tag}'
        em.url = f'http://cr-api.com/profile/{tag}'
        if clan.name is not None:
            em.set_author(name='Profile', icon_url=clan.badge_url)

            em.add_field(name='Level', value=level + '(' + experience + ')')
            em.add_field(name='Arena', value=arena)

            em.add_field(name='Trophies', value=trophies)
            em.add_field(name='Personal Best', value=highest_trophies)
            em.add_field(name='Global Rank', value=global_rank)
            em.add_field(name='Total Donations', value=donations)
            em.add_field(name='Win-Loss Percentage', value=win_percent)
            em.add_field(name='Max Challenge Wins', value=str(profile.max_wins))
            em.add_field(name='Game Record', value=record)

            em.add_field(name='Clan Info', value=clan.name +
                         '\n' + clan.tag + '\n' + profile.clan_role)

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
