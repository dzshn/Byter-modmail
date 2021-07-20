import discord
from discord.ext import commands


class Mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.modmail_channel_id = self.bot.modmail_channel_id
        self.current_dm = None
        self.last_msg_author = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            author = message.author
            self.last_msg_author = author
            await self.bot.get_channel(self.modmail_channel_id).send(
                embed=discord.Embed(
                    color=0x301baa,
                    description=message.content,
                    timestamp=message.created_at,
                ).set_author(
                    name=f'{author} ({author.id})',
                    icon_url=author.avatar_url
                ).set_footer(
                    text=f'ID: {message.id}'
                ),
                files=(
                    [await a.to_file() for a in message.attachments]
                    if message.attachments else None
                )
            )

        elif self.current_dm and message.channel.id == self.modmail_channel_id and not message.content.startswith('m%'):
            await self.last_dm_author.send(message.content)
            await message.add_reaction('📬')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        if isinstance(after.channel, discord.DMChannel):
            author = after.author
            self.last_msg_author = author
            await self.bot.get_channel(self.modmail_channel_id).send(
                embed=discord.Embed(
                    color=0x301baa,
                    description=after.content,
                    timestamp=after.created_at
                ).set_author(
                    name=f'{author} ({author.id})',
                    icon_url=author.avatar_url
                ).set_footer(
                    text=f'ID: {after.id}'
                ).add_field(
                    name=f'Edited, prev.:',
                    value=(
                        before.content[:512] + 
                        ('...' if len(before.content) > 512 else '')
                    )
                ),
                files=(
                    [await a.to_file() for a in after.attachments]
                    if after.attachments else None
                )
            )


    @commands.command(name='set', aliases=['s'])
    async def _set(self, ctx, userid: int):
        user = await self.bot.fetch_user(userid)
        self.current_dm = user
        await ctx.send(f'DM set to {user}')

    @commands.command(aliases=['sl'])
    async def setlast(self, ctx):
        self.current_dm = self.last_msg_author
        await ctx.send(f'DM set to {self.current_dm}')

    @commands.command(aliases=['m'])
    async def message(self, ctx, userid: int, *, text: str):
        user = await self.bot.fetch_user(userid)
        await user.send(text)
        await ctx.message.add_reaction('📬')
        await ctx.send(f'Sent message to {user}')

    @commands.command(aliases=['ml'])
    async def messagelast(self, ctx, *, text: str):
        user = self.last_msg_author
        await user.send(text)
        await ctx.message.add_reaction('📬')
        await ctx.send(f'Sent message to {user}')

    @commands.command(aliases=['c'])
    async def close(self, ctx):
        self.current_dm = None
        await ctx.send('Current DM unset')


def setup(bot):
    bot.add_cog(Mail(bot))
