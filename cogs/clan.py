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
            clan_tag = clan_tag.strip('\#').replace('O', '0')
            clan = await self.client.get_clan(clan_tag)

        try:
            clan = await profile.get_clan()
        except ValueError:
            em.description = 'You are not in a clan'
            return await ctx.send(embed=em)
        except Exception as e:
            pass

        if clan.rank == 0:
            rank = 'Unranked'
        else:
            rank = str(clan.rank)

        chest = str(clan.clan_chest.crowns) + '/' + str(clan.clan_chest.required) + \
            f' ({(clan.clan_chest.crowns / clan.clan_chest.required) * 100:.3f}%)'
        members = str(len(clan.members)) + '/50'

        em.title = clan.name + ' (#' + clan.tag + ')'
        em.set_author(name='Clan Info', icon_url=ctx.author.avatar_url)
        em.description = clan.description

        em.add_field(name='Score', value=str(clan.score))
        em.add_field(name='Required Trophies', value=str(clan.required_trophies))
        em.add_field(name='Donations', value=str(clan.donations))
        em.add_field(name='Region', value=clan.region)
        em.add_field(name='Global Rank', value=rank)
        em.add_field(name='Type', value=clan.type_name)
        em.add_field(name='Clan Chest', value=chest)
        em.add_field(name='Members', value=members)

        em.set_thumbnail(url=clan.badge_url)
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        await ctx.send(embed=em)

    @commands.group(invoke_without_command=True)
    async def members(self, ctx):
        '''A command group that finds the worst and best members in a clan'''
        await ctx.send('Proper usage: `(prefix)members <best|worst>`')

    @members.command()
    async def worst(self, ctx, clan=None):
        '''Find the worst members in a clan'''
        em = discord.Embed(title='Least Valuable Members')
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)

        if clan is None:
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
            clan_tag = clan.strip('\#').replace('O', '0')
            clan = await self.client.get_clan(clan_tag)

        try:
            clan = await profile.get_clan()
        except ValueError:
            em.description = 'You are not in a clan'
            return await ctx.send(embed=em)
        except Exception as e:
            pass

        if len(clan.members) < 4:
            return await ctx.send('Clan must have more than 4 players for stats.')
        else:
            for m in clan.members:
                m.score = ((m.donations / 5) + (m.crowns * 10) + (m.trophies / 7)) / 3

            to_kick = sorted(clan.members, key=lambda m: m.score)[:4]

            em.description = 'Here are the least valuable members of the clan currently.'
            em.set_author(name=clan)
            em.set_thumbnail(url=clan.badge_url)
            em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api.com',
                          icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

            for m in reversed(to_kick):
                em.add_field(name=f'{m.name}, Role: {m.role_name}',
                             value=f"#{m.tag}\n{m.trophies} trophies\n{m.crowns} crowns\n{m.donations} donations")

            await ctx.send(embed=em)

    @members.command()
    async def best(self, ctx, clan=None):
        '''Find the best members in a clan'''
        em = discord.Embed(title='Most Valuable Members')
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)

        if clan is None:
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
            clan_tag = clan.strip('\#').replace('O', '0')
            clan = await self.client.get_clan(clan_tag)

        try:
            clan = await profile.get_clan()
        except ValueError:
            em.description = 'You are not in a clan'
            return await ctx.send(embed=em)
        except Exception as e:
            pass

        if len(clan.members) < 4:
            return await ctx.send('Clan must have more than 4 players for stats.')
        else:
            for m in clan.members:
                m.score = ((m.donations / 5) + (m.crowns * 10) + (m.trophies / 7)) / 3

        best = sorted(clan.members, key=lambda m: m.score, reverse=True)[:4]

        em.description = 'Here are the most valuable members of the clan currently.'
        em.set_author(name=clan)
        em.set_thumbnail(url=clan.badge_url)
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api.com',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

        for m in reversed(best):
            em.add_field(name=f'{m.name}, Role: {m.role_name}',
                         value=f"#{m.tag}\n{m.trophies} trophies\n{m.crowns} crowns\n{m.donations} donations")

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Clan(bot))
