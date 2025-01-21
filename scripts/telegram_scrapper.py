from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

class Scrapper:
    # Function to scrape data from a single channel
    async def scrape_channel(self, client, channel_username, writer):
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title
        async for message in client.iter_messages(entity, limit=10000):
            # Write the channel title along with other data, excluding media path
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date])

    async def main(self):
        # Initialize the client using async with
        async with TelegramClient('scraping_session', api_id, api_hash) as client:
            await client.start()
            
             # Ensure the 'data' directory exists
            os.makedirs('data', exist_ok=True)

            # Open the CSV file and prepare the writer
            with open('data/qnashcom_telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date'])  # Updated header

                # List of channels to scrape
                channels = [
                    '@qnashcom',  # Telegram channel
                ]

                # Scrape data into the CSV file
                for channel in channels:
                    await self.scrape_channel(client, channel, writer)
                    print(f"Scraped data from {channel}")


# Run the scraper
if __name__ == "__main__":
    import asyncio
    scraper = Scrapper()
    asyncio.run(scraper.main())
