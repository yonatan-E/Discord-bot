import discord
from discord.ext import commands

from util.error_handling import create_error_embed
from util.stockx_scraper import (stockx_scraper, stockx_page_finder, stockx_page_scraper)

class stockx_cog(commands.Cog):

    qualified_name = 'stockx'
    description = 'The commands of getting information from stockx.'

    def __init__(self, bot):
        self.__bot = bot

    @commands.command(aliases=['STOCKX', 'StockX'], help='Get information about a stockx product.')
    async def stockx(self, ctx, *, product):

        await ctx.send(embed=discord.Embed(
            title=f'Searching for {product} in StockX. It might take few seconds.',
            colour=discord.Colour.blue()))

        scraper = stockx_scraper(stockx_page_finder(), stockx_page_scraper())
        product_json = scraper.get_product_json(product)

        embed=discord.Embed(
            title="StockX product information",
            description=product_json['product-name'])

        embed.set_thumbnail(url=product_json['image-url'])
        embed.add_field(name='Hightest bid', value=product_json['highest-bid'], inline=True)
        embed.add_field(name='Lowest bid', value=product_json['lowest-bid'], inline=True)
        embed.add_field(name='Last sale', value=product_json['last-sale'], inline=True)
        embed.add_field(name='Retail price', value=product_json['retail-price'], inline=True)
        embed.add_field(name='Release date', value=product_json['release-date'], inline=True)

        await ctx.send(embed=embed)

    @stockx.error
    async def stockx_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=create_error_embed(str(error)))


def setup(bot):
    bot.add_cog(stockx_cog(bot))