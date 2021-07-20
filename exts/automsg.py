import io
import json

import discord
from discord.ext import commands


class AutoMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.automsgs = json.load(open('automsg.json'))

        except FileNotFoundError:
            self.automsgs = []
            json.dump(obj=self.automsgs, fp=open('automsg.json', 'w'))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        for obj in self.automsgs:
            for trigger in obj['triggers']:
                if trigger in message.content:
                    await message.channel.send(
                        obj['response']
                    )

    @commands.group()
    async def automsg(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand or None')

    @automsg.command()
    async def add(self, ctx, *, data):
        triggers, response = data.split('&&&')
        triggers = triggers.split('&&')
        self.automsgs.append(
            {
                "triggers": triggers,
                "response": response
            }
        )

        json.dump(obj=self.automsgs, fp=open('automsg.json', 'w'))

        await ctx.send((
            "Added automsg:\n"
            f"-    with id {len(self.automsgs)-1}\n"
            f"-    with response {response[:80]}...\n"
            f"-    with triggers {', '.join(triggers)}"
        ))

    @automsg.command()
    async def remove(self, ctx, obj_id: int):
        removed = self.automsgs.pop(obj_id)
        json.dump(obj=self.automsgs, fp=open('automsg.json', 'w'))
        await ctx.send((
            "Removed automsg:\n"
            f"-    with id {obj_id}\n"
            f"-    with response {removed['response'][:80]}...\n"
            f"-    with triggers {', '.join(removed['triggers'])}"
        ))

    @automsg.command()
    async def dump(self, ctx):
        await ctx.send(
            file=discord.File(
                open('automsg.json')
            )
        )

    @automsg.command()
    async def write(self, ctx):
        to_write = io.BytesIO
        await ctx.attachments[0].save(to_write)
        try:
            json.dump(
                obj=json.loads(to_write.read()),
                fp=open('automsg.json', 'w')
            )

        except json.JSONDecodeError as error:
            await ctx.send(str(error))

    @automsg.command(name='list')
    async def _list(self, ctx):
        await ctx.send(
            '\n'.join([
                f"id: {index}\n" \
                f"response: {obj['response'][:80]}...\n" \
                f"triggers: {', '.join(obj['triggers'])}"
                for index, obj in enumerate(self.automsgs)
            ])
        )


def setup(bot):
    bot.add_cog(AutoMsg(bot))