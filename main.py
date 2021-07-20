from pathlib import Path

import discord
from discord.ext import commands

class ByterBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=['m%']
        )

        self.add_check(self.global_check)
        self.allowed_role_ids = [
            728875097808699473,
            777720322446983179,
            726615159459676180,
            733954479589687367
        ]

        for i in Path("exts").glob("*.py"):
            if not i.name.startswith('_'):
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
