import discord

async def send_command_error_message(ctx, description):
    await ctx.send(embed=discord.Embed(
        title=f'Couldn\'t complete {ctx.command} command',
        description=description,
        colour=discord.Colour.red()))