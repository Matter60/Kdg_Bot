import discord
import aiohttp
from discord.ext import commands
from datetime import datetime
from icalendar import Calendar
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

class IcsToday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('IcsToday cog is ready.')

    @commands.command(name='today')
    async def ics(self, ctx, *args):
        print("Fetching iCalendar...")
        url = os.getenv('ICS_URL')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch calendar: {response.status}")
                    ical_data = await response.read()
                    print("iCalendar fetched successfully.")
        except Exception as e:
            await ctx.send(f"Failed to fetch the iCalendar data: {e}")
            return

        try:
            calendar = Calendar.from_ical(ical_data)
            print("iCalendar parsed successfully.")
        except Exception as e:
            await ctx.send(f"Failed to parse the iCalendar data: {e}")
            return
        
        # Gebruik Europe/Amsterdam voor GMT+2 tijdzone
        gmt_plus_2 = pytz.timezone('Europe/Amsterdam')
        today = datetime.now(gmt_plus_2).date()
        events_today = []

        for component in calendar.walk():
            if component.name == "VEVENT":
                try:
                    event_name = component.get('summary')
                    location = component.get('location')
                    start = component.get('dtstart').dt
                    end = component.get('dtend').dt
                    description = component.get('description', 'No description available.')

                    # Handle timezone-aware or naive datetime objects
                    if start.tzinfo is None:
                        start = pytz.utc.localize(start).astimezone(gmt_plus_2)
                    else:
                        start = start.astimezone(gmt_plus_2)

                    if end.tzinfo is None:
                        end = pytz.utc.localize(end).astimezone(gmt_plus_2)
                    else:
                        end = end.astimezone(gmt_plus_2)

                    # Check if the event is today in GMT+2
                    if start.date() == today:
                        events_today.append({
                            'name': event_name,
                            'location': location,
                            'start': start,
                            'end': end,
                            'description': description
                        })
                except Exception as e:
                    print(f"Error processing event: {e}")

        if not events_today:
            no_events_embed = discord.Embed(
                title="No Events Today",
                description="There are no scheduled events for today.",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=no_events_embed)
        else:
            embeds = []
            for event in events_today:
                time_range = f"{event['start'].strftime('%H:%M')} - {event['end'].strftime('%H:%M')}"
                
                embed = discord.Embed(
                    title=event['name'],
                    description=event['description'],
                    colour=discord.Colour.blue()
                )
                embed.add_field(name='Location', value=event['location'], inline=False)
                embed.add_field(name='Time', value=time_range, inline=False)
                embeds.append(embed)

            # Send all embeds in one go
            for embed in embeds:
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(IcsToday(bot))
