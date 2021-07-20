import discord
from discord.ext import commands


class Mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mod_channel_id = 784136196229955634
        self.last_dm_author = None
        self.last_msg_author = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            author = message.author
            self.last_msg_author = author
            await self.bot.get_channel(self.mod_channel_id).send(
                embed=discord.Embed(
                    color=0x301baa,
                    title=f'Message from {author} ({author.id})',
                    description=message.content
                )
            )

        elif self.last_dm_author is not None and message.channel.id == self.mod_channel_id and not message.content.startswith('m%'):
            await self.last_dm_author.send(message.content)
            await message.add_reaction('📬')

    @commands.command(name='set', aliases=['s'])
    async def _set(self, ctx, userid: int):
        user = await self.bot.fetch_user(userid)
        self.last_dm_author = user
        await ctx.send(f'DM set to {user}')

    @commands.command(aliases=['sl'])
    async def setlast(self, ctx):
        self.last_dm_author = self.last_msg_author
        await ctx.send(f'DM set to {self.last_dm_author}')

    @commands.command(aliases=['m'])
    async def message(self, ctx, userid: int, *, text: str):
        user = await self.bot.fetch_user(userid)
        await user.send(text)
        await ctx.message.add_reaction('📬')
        await ctx.send(f'Sent message to {user}')

    @commands.command(aliases=['ml'])
    async def messagelast(self, ctx, *, text: str):
        await self.last_msg_author.send(text)
        await ctx.message.add_reaction('📬')
        await ctx.send(f'Sent message to {user}')

    @commands.command(aliases=['c'])
    async def close(self, ctx):
        self.last_dm_author = None
        await ctx.send('Current DM unset')


def setup(bot):
    bot.add_cog(Mail(bot))
