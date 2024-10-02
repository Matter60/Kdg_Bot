import discord
from discord.ext import commands

class Embed(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Embed cog is ready.')

    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(
            title='Title',
            description='Description',
            colour=discord.Colour.blue()
        )

        embed.set_footer(text='Footer')
        embed.set_image(url='https://i.imgur.com/ax0NCsK.jpg')
        embed.set_thumbnail(url='https://i.imgur.com/ax0NCsK.jpg')
        embed.set_author(name='Author', icon_url='https://i.imgur.com/ax0NCsK.jpg')
        embed.add_field(name='Field Name', value='Field Value', inline=False)
        embed.add_field(name='Field Name', value='Field Value', inline=True)
        embed.add_field(name='Field Name', value='Field Value', inline=True)

        await ctx.send(embed=embed)


async def setup(client):
   await client.add_cog(Embed(client))


