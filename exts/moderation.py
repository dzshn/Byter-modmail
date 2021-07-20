import typing

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for role in message.author.roles:
            if role.id == 776212011050467348:
                await message.delete()

    @commands.command()
    async def delete(self, ctx, *messages: discord.Message):
        if len(messages) > 1:
            for message in messages:
                await message.delete()
                await ctx.send(f'Deleted message {message}', delete_after=5)

            await ctx.message.add_reaction('🗑')

        else:
            await messages[0].delete()
            await ctx.message.add_reaction('🗑')


def setup(bot):
    bot.add_cog(Moderation(bot))
