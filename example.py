import asyncio
import sys
from geopy.geocoders import Nominatim


from wrapper.assistant import VoiceAssistant
import time
client=VoiceAssistant(name="Example")

@client.command(keyword="time")
async def get_time():
    """Get the current time."""
    current_time = time.strftime("%I:%M %p")
    return f"The current time is {current_time}."

@client.command(keyword="location")
async def get_location(place):
    """Get the coordinates of a place."""
    try:
        location = self.loc.geocode(place)
        if location:
            return f"The coordinates of {place} are Latitude: {location.latitude}, Longitude: {location.longitude}"
        else:
            return f"Location {place} not found."
    except Exception as e:
        return f"Failed to retrieve location information: {e}"

# Example usage
async def main():
    await client.listen()

# Run the main function
asyncio.run(main())
