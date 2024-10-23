import os
import discord
from dotenv import load_dotenv
from db import Database
from scraper import MessageScraper

def main():
    load_dotenv()
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')

    if not all([TOKEN, CHANNEL_ID]):
        print("Error: Please set DISCORD_TOKEN and CHANNEL_ID in .env file")
        return

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guild_messages = True

    db = Database()
    client = MessageScraper(
        db=db,
        channel_id=CHANNEL_ID,
        intents=intents
    )

    print("Starting Discord message scraper...")
    client.run(TOKEN)

if __name__ == "__main__":
    main()