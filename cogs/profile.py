import discord
from discord.ext import commands
import crasync
import aiohttp
import json
import os


class Profile:
    '''Get info about your Profile'''

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

    def cdir(self, obj):
        return [x for x in dir(obj) if not x.startswith('_')]

    def get_chests(self, ctx, p):
        cycle = p.chest_cycle
        pos = cycle.position
        chests = p.get_chest(0).title() + '\n'
        chests += '\n'.join([p.get_chest(x).title() for x in range(1, 8)])
        special = ''
        for i, attr in enumerate(self.cdir(cycle)):
            if attr != 'position':
                e = attr.replace('_', '')
                if getattr(cycle, attr):
                    c_pos = int(getattr(cycle, attr))
                    until = c_pos - pos
                    special += f'{e.title()}+{until} '
                    return (chests, special)

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

        try:
            clan = await profile.get_clan()
        except ValueError:
            pass

        if profile.global_rank is not None:
            global_rank = str(profile.global_rank)
        else:
            global_rank = 'Unranked'
        experience = f'{profile.experience[0]}/{profile.experience[1]}'
        record = f'{profile.wins}-{profile.draws}-{profile.losses}'
        av = profile.clan_badge_url or 'https://i.imgur.com/Y3uXsgj.png'

        chests = self.get_chests(ctx, profile)[0]
        cycle = profile.chest_cycle
        pos = cycle.position
        special = ''

        s = None
        if profile.seasons:
            s = profile.seasons[0]
            global_r = s.end_global
            season = f"Highest: {s.highest} trophies\n" \
                     f"Finish: {s.ending} trophies\n" \
                     f"Global Rank: {global_r}"
        else:
            season = None

        special = self.get_chests(ctx, profile)[1]
        shop_offers = ''
        if profile.shop_offers.legendary:
            shop_offers += f"Legendary Chest: {profile.shop_offers.legendary} days\n"
        if profile.shop_offers.epic:
            shop_offers += f"Epic Chest: {profile.shop_offers.epic} days\n"
        if profile.shop_offers.arena:
            shop_offers += f"Arena: {profile.shop_offers.arena} days\n"

        deck = ''
        for card in profile.deck:
            deck += f'{card.name}: Lvl {card.level}\n'

        em.title = profile.name
        em.description = f'#{tag}'
        em.url = f'http://cr-api.com/profile/{tag}'
        em.set_author(name='Profile', icon_url=av)

        em.add_field(name='Level', value=f'{level} ({experience})')
        em.add_field(name='Arena', value=profile.arena.name)

        em.add_field(
            name='Trophies', value=f'{profile.current_trophies}/{profile.highest_trophies}(PB)/{profile.legend_trophies} LEGEND')
        em.add_field(name='Global Rank', value=global_rank)
        em.add_field(name='Total Donations', value=f'{profile.total_donations}')
        em.add_field(name='Win Percentage',
                     value=f'{(profile.wins / (profile.wins + profile.losses)*100):.3f}%')
        em.add_field(name='Max Challenge Wins', value=f'{profile.max_wins}')
        em.add_field(name='Favorite Card', value=profile.favourite_card)
        em.add_field(name='Game Record (Win Streak)', value=f'{record} ({profile.win_streak})')

        if profile.clan_role:
            em.add_field(name='Clan Info', value=f'{clan.name}\n#{clan.tag}\n{profile.clan_role}')
        else:
            em.add_field(name='Clan Info', value='No clan')

        em.add_field(name='Tournament Cards Won', value=str(profile.tournament_cards_won))
        em.add_field(name='Challenge Cards Won', value=str(profile.challenge_cards_won))
        em.add_field(name='Battle Deck', value=deck)
        em.add_field(name=f'Chests (Total {pos} opened)', value=chests)
        em.add_field(name='Chests Until', value=special)
        em.add_field(name='Shop Offers', value=shop_offers)
        if s:
            em.add_field(name=f'Previous Season Results (Season {s.number})', value=season)
        else:
            pass

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
        em.set_author(
            name='Trophies', icon_url='http://clashroyalehack1.com/wp-content/uploads/2017/06/coctrophy.png')
        em.description = f'Trophies: `{profile.current_trophies}`\nPersonal Best: `{profile.highest_trophies}`\nLegend Trophies: `{profile.legend_trophies}`'
        em.set_thumbnail(
            url='http://vignette1.wikia.nocookie.net/clashroyale/images/7/7c/LegendTrophy.png/revision/latest?cb=20160305151655')
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)

    @commands.command()
    async def deck(self, ctx, tag=None):
        '''View a player's deck'''
        em = discord.Embed(title='Battle Deck')
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

        deck = ''
        for card in profile.deck:
            deck += f'{card.name}: Lvl {card.level}\n'

        em.title = profile.name
        em.set_author(name='Battle Deck', icon_url=ctx.author.avatar_url)
        em.description = deck
        em.set_thumbnail(
            url='https://cdn.discordapp.com/emojis/376367875965059083.png')
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

        em.url = f'http://cr-api.com/profile/{tag}'
        em.title = profile.name
        em.add_field(name='URL', value=f'http://cr-api.com/profile/{tag}')
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Profile(bot))
