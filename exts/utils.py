import io
import typing

import discord


def format_output(text: str) -> (str, typing.Optional[discord.File]):
    """Helper function for cleaning and colapsing outputs"""
    out = text.replace('`', "'")
    att = None
    if out == '':
        out = '<No output>'

    elif len(out) > 1500:
        out = out[:1500]+'\n[...]'
        att = discord.File(io.StringIO(text), filename='output.txt')

    return out, att
