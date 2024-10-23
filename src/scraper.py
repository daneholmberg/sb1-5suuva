import discord
import asyncio
from datetime import datetime

class MessageScraper(discord.Client):
    def __init__(self, db, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db
        self.channel_id = int(channel_id)
        self.FETCH_LIMIT = 100
        self.INTERVAL = 60  # seconds

    async def fetch_messages(self, channel, before_id=None):
        try:
            kwargs = {'limit': self.FETCH_LIMIT}
            if before_id:
                kwargs['before'] = discord.Object(id=before_id)
            
            messages = [msg async for msg in channel.history(**kwargs)]
            
            if not messages:
                return False

            for message in messages:
                self.db.save_message(message)
            
            return True

        except Exception as e:
            print(f"Error fetching messages: {e}")
            return False

    async def scrape_channel(self):
        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"Channel {self.channel_id} not found")
            return

        print(f"Starting to scrape channel: {self.channel_id}")
        
        has_more = True
        last_message_id = self.db.get_last_message_id(self.channel_id)

        while has_more:
            has_more = await self.fetch_messages(channel, last_message_id)
            if has_more:
                last_message_id = self.db.get_last_message_id(self.channel_id)
                print(f"Fetched batch of messages before ID: {last_message_id}")

        print("Reached end of channel history")

    async def start_scraping(self):
        while True:
            await self.scrape_channel()
            print(f"Waiting {self.INTERVAL} seconds before next scan...")
            await asyncio.sleep(self.INTERVAL)

    async def setup_hook(self):
        self.loop.create_task(self.start_scraping())