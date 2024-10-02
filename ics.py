# import discord
# import requests
# from discord.ext import commands
# from datetime import datetime
# from icalendar import Calendar


# class Ics(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
    
#     @commands.Cog.listener()
#     async def on_ready(self):
#         print('Ics cog is ready.')

#     @commands.command()
#     async def ics(self, ctx):
#         print("Fetching iCalendar...")
#         url = 'https://cloud.timeedit.net/be_kdg/web/student/ri6Y35wlyZ5ZQjQ16d5QZ1m25681Q1kQ98oZ0nZQ87347unu230t813Z2B8C8815oj206BF16tkElF665932D6A512EQ7553.ics'
       
#         response = requests.get(url)

#         if response.status_code == 200:
#             ical_data = response.text
#             calendar = Calendar.from_ical(ical_data)

#             for component in calendar.walk():
#                 if component.name == "VEVENT":
#                     event_name = component.get('summary')
#                     start = component.get('dtstart').dt
#                     end = component.get('dtend').dt
#                     description = component.get('description')

#                     embed = discord.Embed(
#                         title=event_name,
#                         description=description,
#                         colour=discord.Colour.blue()
#                     )

#                     embed.add_field(name='Start', value=start, inline=False)
#                     embed.add_field(name='End', value=end, inline=False)

#                     await ctx.send(embed=embed)
#         else:
#             await ctx.send(f"Failed to fetch the iCalendar data. Status code: {response.status_code}")
            


# async def setup(bot):
#     await bot.add_cog(Ics(bot))
