from pathlib import Path

import discord
from discord.ext import commands

import config


class ByterBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.prefixes
        )

        self.add_check(self.global_check)
        self.allowed_role_ids = config.allowed_role_ids
        self.modmail_channel_id = config.modmail_channel_id

        for i in Path("exts").glob("*.py"):
            try:
                self.load_extension(str(i)[:-3].replace('/', '.'))

            except commands.ExtensionError:
                pass

    async def global_check(self, ctx):
        if ctx.author.top_role.id in self.allowed_role_ids:
            return True

        raise commands.MissingRole


bot = ByterBot()
bot.run(open("TOKEN").read())
