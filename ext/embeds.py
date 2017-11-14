import discord
from collections import OrderedDict
import json


def cdir(obj):
    return [x for x in dir(obj) if not x.startswith('_')]


def get_deck(ctx, p):
    deck = {}
    aoe = 0
    for card in p.deck:
        deck[card.name] = f'Lvl {card.level}'
        aoe += card.elixir
    aoe = f'{(aoe / 8):.3f}'
    return (deck, aoe)


async def format_least_valuable(ctx, clan):

    em = discord.Embed(title='Least Valuable Members')
    em.color = await ctx.get_dominant_color(ctx.author.avatar_url)

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

    return em


async def format_most_valuable(ctx, clan):
    em = discord.Embed(title='Most Valuable Members')
    em.color = await ctx.get_dominant_color(ctx.author.avatar_url)

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

    return em


def get_chests(ctx, p):
    cycle = p.chest_cycle
    pos = cycle.position
    chests = p.get_chest(0).title() + '\n'
    chests += '\n'.join([p.get_chest(x).title() for x in range(1, 8)])
    special = ''
    for i, attr in enumerate(cdir(cycle)):
        if attr != 'position':
            e = attr.replace('_', '')
            if getattr(cycle, attr):
                c_pos = int(getattr(cycle, attr))
                until = c_pos - pos
                special += f'{e.title()}+{until} '
    return (chests, special)


async def format_deck(ctx, p):
    em = discord.Embed(title='Battle Deck')
    em.color = await ctx.get_dominant_color(ctx.author.avatar_url)

    av = p.clan_badge_url or 'https://i.imgur.com/Y3uXsgj'
    em.set_author(name=p, icon_url=av)
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/376367875965059083.png')
    em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api.com',
                  icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

    pdeck = get_deck(ctx, p)[0]
    for c, l in pdeck.items():
        em.add_field(name=c, value=l)
    aoe = get_deck(ctx, p)[1]
    em.add_field(name='Average Elixir Cost', value=aoe)
    return em


async def format_chests(ctx, p):
    av = p.clan_badge_url or 'https://i.imgur.com/Y3uXsgj.png'
    em = discord.Embed(title='Chests')
    em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
    em.set_author(name=p, icon_url=av)
    em.set_thumbnail(url='http://www.oyunincele.me/clash/chests/legendary-chest.png')
    em.add_field(
        name=f'Chests (Total {p.chest_cycle.position} opened)', value=get_chests(ctx, p)[0])
    em.add_field(name='Chests Until', value=get_chests(ctx, p)[1])
    em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api.com',
                  icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

    return em


async def format_card(ctx, c):
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
    em = discord.Embed(description=c.description)
    em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
    em.set_thumbnail(url='attachment://card.png')
    em.set_author(name='Card Info', icon_url=ctx.author.avatar_url)
    em.add_field(name='Rarity', value=c.rarity)
    em.add_field(name='Type', value=c.type)
    em.add_field(name='Arena', value=arenas[c.arena])
    em.add_field(name='Cost', value=f'{c.elixir} elixir')
    em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api.com',
                  icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

    return em


async def format_profile(ctx, p):
    av = p.clan_badge_url or 'https://i.imgur.com/Y3uXsgj.png'
    em = discord.Embed(color=await ctx.get_dominant_color(ctx.author_url))
    em.set_author(name='Profile', icon_url=av)
    em.title = p.name
    em.description = f'#{p.tag}'
    em.url = f'http://cr-api.com/profile/{tag}'
    em.set_thumbnail(url=p.arena.image_url)

    deck = get_deck(ctx, p)
    chests = get_chests(ctx, p)[0]
    cycle = p.chest_cycle
    pos = cycle.position
    special = ''
    trophies = p.current_trophies + '/' + p.highest_trophies + \
        '(PB)/' + p.legend_trophies + ' Legend'

    s = None
    if p.seasons:
        s = p.seasons[0]
        global_r = s.end_global
        season = f"Highest: {s.highest} trophies\n" \
                 f"Finish: {s.ending} trophies\n" \
                 f"Global Rank: {global_r}"
    else:
        season = None

    special = get_chests(ctx, p)[1]
    win_percent = f'{(p.wins / (p.wins + p.losses)*100):.3f}%'
    record = f'{p.wins}-{p.draws}-{p.losses}'

    shop_offers = ''
    if p.shop_offers.legendary:
        shop_offers += f"Legendary Chest: {p.shop_offers.legendary} days\n"
    if p.shop_offers.epic:
        shop_offers += f"Epic Chest: {p.shop_offers.epic} days\n"
    if p.shop_offers.arena:
        shop_offers += f"Arena: {p.shop_offers.arena} days\n"

    embed_fields = [
        ('Level', f"{p.level} ({'/'.join(str(x) for x in p.experience)})"),
        ('Arena', p.arena.name),
        ('Trophies', trophies),
        ('Global Rank', f'{p.global_rank}' if p.global_rank is not 0 else None),
        ('Total Donations', f'{p.total_donations}'),
        ('Win Percentage', win_percent),
        ('Max Challenge Wins', f'{p.max_wins}'),
        ('Favorite Card', p.favourite_card.replace('_', ' ')),
        ('Game Record (Win Streak)', f'{record} ({p.win_streak})'),
        ('Clan Info', f'{p.clan_name}\n{p.clan_tag}\n{p.clan_role}' if p.clan_role else None),
        ('Tournament Cards Won', f'{p.tournament_cards_won}'),
        ('Challenge Cards Won', f'{p.challenge_cards_won}'),
        ('Battle Deck', deck),
        (f'Chests (Total {pos} opened)', chests),
        ('Chests Until', special)
        ('Shop Offers', shop_offers),
        (f'Previous Season Results (Season {s.number})' if s else None, season)
    ]

    for n, v in embed_fields:
        if v:
            em.add_field(name=n, value=v)
        else:
            if n == 'Global Rank':
                em.add_field(name=n, value='Unranked')
            if n == 'Clan Info':
                em.add_field(name=n, value='No Clan')
    em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api.com',
                  icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

    return em


async def format_clan(ctx, c):
    em = discord.Embed(description=c.description, color=await ctx.get_dominant_color(ctx.author_url))
    em.set_author(name='Clan Info', icon_url=ctx.author.avatar_url)
    em.title = f'{c.name} #{c.tag}'
    em.set_thumbnail(url=c.badge_url)
    em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                  icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')

    pushers = []
    if len(c.members) >= 3:
        for i in range(3):
            pushers.append(
                f"**{c.members[i].name}**\n{c.members[i].trophies} trophies\n#{c.members[i].tag}")
    contributors = list(reversed(sorted(c.members, key=lambda x: x.crowns)))

    ccc = []
    if len(c.members) >= 3:
        for i in range(3):
            ccc.append(
                f"**{contributors[i].name}**\n{contributors[i].crowns} crowns\n#{contributors[i].tag}")

    if c.rank == 0:
        rank = 'Unranked'
    else:
        rank = f'{c.rank}'

    chest = f'{c.clan_chest.crowns}/{c.clan_chest.required} ({(c.clan_chest.crowns / c.clan_chest.required) * 100:.3f}%)'

    em = OrderedDict({
        'Score': f'{c.score}',
        'Required Trophies': f'{c.required_trophies}',
        'Donations': f'{c.donations}',
        'Region': c.region,
        'Global Rank': rank,
        'Type': c.type_name,
        'Clan Chest': chest,
        'Members': f'{len(c.members)}/50',
        'Top Players': '\n\n'.join(pushers),
        'Top Contributors': '\n\n'.join(ccc),
    })

    for f, v in em.items():
        em.add_field(name=f, value=v)

    return em
