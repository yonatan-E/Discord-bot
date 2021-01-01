import discord
from discord.ext import commands

import os

TOKEN = 'NzkzOTE2MzY0ODA4OTEyOTQ3.X-zOOw._kfipXmWQV5j38uf3WIDETvTFZM'

class discord_bot(commands.Bot):

    VERSION = 1.0

    def __init__(self):
        super().__init__(command_prefix='$', help_command=None)

        # loading the cogs
        for file_name in os.listdir('./extensions'):
            if file_name.endswith('.py'):
                super().load_extension(f'extensions.{file_name[:-3]}')


if __name__ == '__main__':
    bot = discord_bot()
    bot.run(TOKEN)