import discord
from discord.ext import commands
from ext import embeds
from __main__ import InvalidTag
import crasync
import aiohttp
import json
import os


class TagCheck(commands.MemberConverter):

    check = 'PYLQGRJCUV0289'

    def resolve_tag(self, tag):
        tag = tag.strip('#').upper().replace('O', '0')

        if any(i not in self.check for i in tag):
            return False
        else:
            return tag

    async def convert(self, ctx, argument):
        tag = self.resolve_tag(argument)
        if not tag:
            raise InvalidTag('Invalid tag passed')
        else:
            return tag


class Clan:
    '''Get info about a clan'''

    def __init__(self, bot):
        self.bot = bot
        self.cr = bot.cr
        self.conv = TagCheck()

    async def get_clan_from_profile(self, ctx, tag, message):
        profile = await self.cr.get_profile(tag)
        clan_tag = profile.clan_tag
        if clan_tag is None:
            await ctx.send(message)
            raise ValueError(message)
        else:
            return clan_tag

    async def resolve_tag(self, ctx, tag, clan=False):
        if not tag:
            try:
                tag = ctx.get_tag()
            except Exception as e:
                print(e)
                await ctx.send('Add your tag to your config vars')
                raise e
            else:
                if clan is True:
                    return await self.get_clan_from_profile(ctx, tag, 'You are not in a clan!')
                return tag

    @commands.command()
    async def clan(self, ctx, clan_tag=None):
        tag = await self.resolve_tag(ctx, clan_tag, clan=True)

        try:
            clan = await self.cr.get_clan(tag)
        except Exception as e:
            return await ctx.send(f'`{e}`')
        else:
            em = await embeds.format_clan(ctx, clan)
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
