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
        win_decimal = f'{(profile.wins / (profile.wins + profile.losses)*100):.3f}'
        win_percent = win_decimal + '%'
        record = str(profile.wins) + '-' + str(profile.draws) + '-' + str(profile.losses)

        deck = profile.deck
        deck_levels = {}
        for card in deck:
            deck_levels[card.name] = 'Lvl ' + str(card.level)
        fmt = ''
        for key, value in deck_levels.items():
            fmt += key + ': ' + value + '\n'

        em.title = profile.name
        em.description = f'#{tag}'
        em.url = f'http://cr-api.com/profile/{tag}'
        if clan.name is not None:
            em.set_author(name='Profile', icon_url=clan.badge_url)

            em.add_field(name='Level', value=level + ' (' + experience + ')')
            em.add_field(name='Arena', value=arena)

            em.add_field(name='Trophies', value=trophies)
            em.add_field(name='Personal Best', value=highest_trophies)
            em.add_field(name='Global Rank', value=global_rank)
            em.add_field(name='Total Donations', value=donations)
            em.add_field(name='Win-Loss Percentage', value=win_percent)
            em.add_field(name='Max Challenge Wins', value=str(profile.max_wins))
            em.add_field(name='Favorite Card', value=profile.favourite_card)
            em.add_field(name='Game Record', value=record)

            em.add_field(name='Clan Info', value=clan.name +
                         '\n#' + clan.tag + '\n' + profile.clan_role)

            em.add_field(name='Tournament Cards Won', value=str(profile.tournament_cards_won))
            em.add_field(name='Challenge Cards Won', value=str(profile.challenge_cards_won))
            em.add_field(name='Battle Deck', value=fmt)

            em.set_thumbnail(url=profile.arena.image_url)
            em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                          icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        else:
            em.set_author(name='Profile')
            em.add_field(name='Level', value=level + '(' + experience + ')')
            em.add_field(name='Arena', value=arena)

            em.add_field(name='Trophies', value=trophies)
            em.add_field(name='Personal Best', value=highest_trophies)
            em.add_field(name='Global Rank', value=global_rank)
            em.add_field(name='Total Donations', value=donations)
            em.add_field(name='Win-Loss Percentage', value=win_percent)
            em.add_field(name='Max Challenge Wins', value=str(profile.max_wins))
            em.add_field(name='Favorite Card', value=profile.favourite_card)
            em.add_field(name='Game Record', value=record)

            em.add_field(name='Clan Info', value='No clan')
            em.add_field(name='Tournament Cards Won', value=str(profile.tournament_cards_won))
            em.add_field(name='Challenge Cards Won', value=str(profile.challenge_cards_won))
            em.add_field(name='Battle Deck', value=fmt)

            em.set_thumbnail(url=profile.arena.image_url)
            em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                          icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)

    @commands.command()
    async def trophies(self, ctx, tag=None):
        '''See your current, record, and legend trophies'''
        em = discord.Embed(title='Trophies')
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

        trophies = str(profile.current_trophies)
        highest_trophies = str(profile.highest_trophies)
        legend_trophies = str(profile.legend_trophies)

        em.title = profile.name
        em.set_author(name='Trophies', icon_url=profile.arena.image_url)
        em.description = 'Trophies: `' + trophies + '`\nPersonal Best: `' + \
            highest_trophies + '`\nLegend Trophies: `' + legend_trophies + '`'
        em.set_thumbnail(
            url='http://vignette1.wikia.nocookie.net/clashroyale/images/7/7c/LegendTrophy.png/revision/latest?cb=20160305151655')
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)

    @commands.command()
    async def weburl(self, ctx, tag=None):
        '''Get the cr-api.com url for a tag'''
        em = discord.Embed(title='cr-api.com URL')
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

        em.url = 'http://cr-api.com/profile/{tag}'
        em.title = profile.name
        em.add_field(name='URL', value='http://cr-api.com/profile/{tag}')
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Profile(bot))
