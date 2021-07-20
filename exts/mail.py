import discord
from discord.ext import commands

from . import utils # pylint: disable=relative-beyond-top-level


class Mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mod_channel_id = 784136196229955634
        self.last_dm = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            author = message.author
            self.last_dm = author
            out, att = utils.format_output(message.content)
            await self.bot.get_channel(self.mod_channel_id).send(
                embed=discord.Embed(
                    color=0x301baa,
                    title=f'Message from {author} ({author.id})',
                    description=out
                ),
                file=att
            )

        elif self.last_dm is not None and message.channel.id == self.mod_channel_id and not message.content.startswith('m%'):
            await self.last_dm.send(message.content)

    @commands.command(name='set', aliases=['s'])
    async def _set(self, ctx, user: discord.User):
        self.last_dm = user
        await ctx.send(f'DM set to {user}')

    @commands.command(aliases=['c'])
    async def close(self, ctx):
        self.last_dm = None
        await ctx.send('Current DM unset')


def setup(bot):
    bot.add_cog(Mail(bot))
