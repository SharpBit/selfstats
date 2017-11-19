import discord
from discord.ext import commands
from ext.colors import ColorNames
from ext import embedtobox
from PIL import Image
import inspect
import io


def random_color(self):
    color = ('#%06x' % random.randint(8, 0xFFFFFF))
    color = int(color[1:], 16)
    color = discord.Color(value=color)
    return color


class Utility:
    '''Useful commands to make your life easier'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='logout')
    async def _logout(self, ctx):
        '''
        Shuts down the selfbot,
        equivalent to a restart if you are hosting on heroku
        '''
        await ctx.send('`Selfbot Logging out...`')
        await self.bot.logout()

    @commands.command(name='help')
    async def new_help_command(self, ctx, *commands: str):
        '''Shows this message.'''
        destination = ctx.message.author if self.bot.pm_help else ctx.message.channel

        def repl(obj):
            return self.bot._mentions_transforms.get(obj.group(0), '')

        # help by itself just lists our own commands.
        if len(commands) == 0:
            pages = await self.bot.formatter.format_help_for(ctx, self.bot)
        elif len(commands) == 1:
            # try to see if it is a cog name
            name = self.bot._mention_pattern.sub(repl, commands[0])
            command = None
            if name in self.bot.cogs:
                command = self.bot.cogs[name]
            else:
                command = self.bot.all_commands.get(name)
                if command is None:
                    await destination.send(self.bot.command_not_found.format(name))
                    return

            pages = await self.bot.formatter.format_help_for(ctx, command)
        else:
            name = self.bot._mention_pattern.sub(repl, commands[0])
            command = self.bot.all_commands.get(name)
            if command is None:
                await destination.send(self.bot.command_not_found.format(name))
                return

            for key in commands[1:]:
                try:
                    key = self.bot._mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await destination.send(self.bot.command_not_found.format(key))
                        return
                except AttributeError:
                    await destination.send(self.bot.command_has_no_subcommands.format(command, key))
                    return

            pages = await self.bot.formatter.format_help_for(ctx, command)

        if self.bot.pm_help is None:
            characters = sum(map(lambda l: len(l), pages))
            # modify destination based on length of pages.
            if characters > 1000:
                destination = ctx.message.author

        color = random.color()

        for embed in pages:
            em = discord.Embed(title='Command Help', color=color)
            embed = embed.strip('```')
            em.description = embed
            try:
                await ctx.send(embed=em)
            except discord.HTTPException:
                em_list = await embedtobox.etb(embed)
                for page in em_list:
                    await ctx.send(page)

    @commands.command()
    async def dcolor(self, ctx, *, url):
        '''A command that gets the dominant color of an image url'''
        await ctx.message.delete()
        color = await ctx.get_dominant_color(url)
        string_col = ColorNames.color_name(str(color))
        info = f'`{str(color)}`\n`{color.to_rgb()}`\n`{str(string_col)}`'
        em = discord.Embed(color=color, title='Dominant Color', description=info)
        em.set_thumbnail(url=url)
        em.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                      icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
        file = io.BytesIO()
        Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        em.set_image(url="attachment://color.png")
        await ctx.send(file=discord.File(file, 'color.png'), embed=em)

    @commands.command()
    async def tinyurl(self, ctx, *, link: str):
        '''Makes a link shorter using the tinyurl api'''
        await ctx.message.delete()
        url = 'http://tinyurl.com/api-create.php?url=' + link
        async with ctx.session.get(url) as resp:
            new = await resp.text()
        emb = discord.Embed(color=random.color())
        emb.add_field(name="Original Link", value=link, inline=False)
        emb.add_field(name="Shortened Link", value=new, inline=False)
        emb.set_footer(text='Selfbot made by SharpBit | Powered by cr-api',
                       icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
        await ctx.send(embed=emb)

    @commands.command()
    async def hastebin(self, ctx, *, code):
        '''Hastebin-ify your code!'''
        async with ctx.session.post("https://hastebin.com/documents", data=code) as resp:
            data = await resp.json()
            key = data['key']
        await ctx.message.edit(content=f"Hastebin-ified! <https://hastebin.com/{key}.py>")

    @commands.command()
    async def source(self, ctx, *, command):
        '''See the source code for any command.'''
        source = str(inspect.getsource(self.bot.get_command(command).callback))
        fmt = '```py\n' + source.replace('`', '\u200b`') + '\n```'
        if len(fmt) > 2000:
            async with ctx.session.post("https://hastebin.com/documents", data=source) as resp:
                data = await resp.json()
            key = data['key']
            return await ctx.send(f'Command source: <https://hastebin.com/{key}.py>')
        else:
            return await ctx.send(fmt)


def setup(bot):
    bot.add_cog(Utility(bot))
