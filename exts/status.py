from discord.ext import commands, tasks
import discord


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes_string = ', '.join(self.bot.config.prefixes)
        self.prefixes_string = self.prefixes_string.replace(', ', ' or ', -1)
        self.update_status.start() # pylint: disable=no-member

    @tasks.loop(minutes=5.0)
    async def update_status(self):
        await self.bot.change_presence(
            activity=discord.Game(
                f"at {len(self.bot.guilds)} servers! My prefix is {self.prefixes_string}"
            )
        )

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Status(bot))
