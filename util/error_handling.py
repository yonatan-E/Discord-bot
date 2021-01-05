import discord

def create_error_embed(description):
    return discord.Embed(
        title=f'Couldn\'t complete command',
        description=description,
        colour=discord.Colour.red())