import io
import subprocess
import traceback
import typing
import textwrap
import contextlib

from discord.ext import commands
import discord

from . import utils # pylint: disable=relative-beyond-top-level


class Admin(commands.Cog, command_attrs={'hidden': True}):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return True

        raise commands.NotOwner

    @commands.command(name="eval", aliases=["e"])
    async def _eval(self, ctx, *, code):
        """Evaluates given code, useful for testing"""
        eval_stdout = io.StringIO()
        env = {}
        env.update(globals())
        env.update(locals())
        if code.startswith('```') and code.endswith('```'):
            code = '\n'.join(code.split('\n')[1:-1])
            code = "async def func():\n"+textwrap.indent(code, "  ")

        else:
            code = code.strip('` \n')
            code = f"async def func(): print({code})"

        try:
            exec(code ,env)
            with contextlib.redirect_stdout(eval_stdout):
                await env['func']()

        except:
            out, att = utils.format_output(traceback.format_exc())
            await ctx.send(
                embed=discord.Embed(
                    color=0xfa0505,
                    title=":x: Error!",
                    description=f"**Traceback:**```py\n{out}\n```"
                ),
                file=att
            )

        else:
            out, att = utils.format_output(eval_stdout.getvalue())

            await ctx.send(
                embed=discord.Embed(
                    color=0x05ba05,
                    title="Code Evaluated with success :white_check_mark:",
                    description=f"```py\n{out}\n```"
                ),
                file=att
            )

    @commands.command(aliases=["sh"])
    async def shell(self, ctx, *, command):
        """Runs given shell command"""
        try:
            out, att = utils.format_output(
                subprocess.run(
                    command, capture_output=True,
                    text=True, shell=True, check=True
                ).stdout
            )

            await ctx.send(
                embed=discord.Embed(
                    color=0x05ba05,
                    title=':white_check_mark: Process ended with exit code 0',
                    description=f"```\n{out}\n```"
                ),
                file=att
            )

        except subprocess.CalledProcessError as exc:
            out, att = utils.format_output(exc.output)
            await ctx.send(
                embed=discord.Embed(
                    color=0xfa0505,
                    title=f":x: Error! process ended with non-zero status ({exc.returncode})",
                    description=f"```\n{out}\n```"
                ),
                file=att
            )

    @commands.group(aliases=["ext"])
    async def extension(self, ctx):
        """Simple extension manager for quick updating, uses the exts folder automatically"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @extension.command(name="list", aliases=["ls"])
    async def extension_list(self, ctx):
        """Lists loaded extensions"""
        await ctx.send(
            embed=discord.Embed(
                title=f"Loaded cogs: ({len(self.bot.cogs)})",
                description=f"`{'`, `'.join(self.bot.cogs)}`"
            )
        )

    @extension.command(name="reload", aliases=["r"])
    async def extension_reload(self, ctx, *exts):
        """Reloads given extensions"""
        for ext in exts:
            try:
                self.bot.reload_extension("exts."+ext)
                await ctx.send(f'Extension exts.{ext} reloaded!')

            except commands.ExtensionError as exc:
                await ctx.send(exc)

    @extension.command(name="load", aliases=["l"])
    async def extension_load(self, ctx, *exts):
        """Loads given extensions"""
        for ext in exts:
            try:
                self.bot.load_extension("exts."+ext)
                await ctx.send(f'Extension exts.{ext} loaded!')

            except commands.ExtensionError as exc:
                await ctx.send(exc)

    @extension.command(name="unload", aliases=["u"])
    async def extension_unload(self, ctx, *exts):
        """Unloads given extensions"""
        for ext in exts:
            try:
                self.bot.unload_extension("exts."+ext)
                await ctx.send(f'Extension exts.{ext} unloaded!')

            except commands.ExtensionError as exc:
                await ctx.send(exc)

    @commands.command()
    async def say(self, ctx, where: typing.Optional[discord.TextChannel]=None, *, text):
        """Sends given text and deletes the command message, optionaly takes a channel"""
        if where is None:
            await ctx.send(text)
            await ctx.message.delete()

        else:
            await where.send(text)


def setup(bot):
    bot.add_cog(Admin(bot))
