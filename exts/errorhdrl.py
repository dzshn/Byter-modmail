import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(
            embed=discord.Embed(
                color=0xfa0505,
                title="**Error!**",
                description=(
                    f"**On command :** {ctx.command}\n"
                    f"**Message content :** {ctx.message.content}\n"
                    f"**Error :** {error}\n"
                )
            )
        )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
