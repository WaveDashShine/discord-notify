import time
import random
import asyncio
import discord
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from configs import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from debug.debug_log import logger
from manhwa_checker.main import get_manhwa_updates
from manhwa_checker.timer import Timer
from datetime import datetime
from manhwa_checker.pages.asura import Chapter


POLLING_RATE = 60  # minutes


async def send_message(chapter_list: list[Chapter]):
    """
    # Message Intent: required for sending and receiving messages
    - set in Discord API portal
    """
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        logger.info(f"Channel: {channel}")
        for chapter in chapter_list:
            await channel.send(f"{chapter}\n{chapter.link}")
        await client.close()

    await client.start(token=DISCORD_TOKEN)
    # await client.run(DISCORD_TOKEN)  # blocking


def main():
    timer = Timer()  # instantiate based on log time
    locked_chapters: list[Chapter] = []
    while True:
        logger.info(f"Checking at {datetime.now()}")
        try:
            chapter_list: list[Chapter] = get_manhwa_updates(
                timer=timer, locked_chapters=locked_chapters
            )
            if chapter_list:
                logger.info(f"New chapters: {chapter_list}")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(send_message(chapter_list))
        except PlaywrightTimeoutError as e:
            logger.error(e)
        timer = Timer()
        polling_rate_seconds = 60 * POLLING_RATE
        time_to_sleep: int = random.randrange(
            start=int(polling_rate_seconds * 0.9), stop=int(polling_rate_seconds * 1.1)
        )
        logger.info(f"sleeping for {time_to_sleep} seconds")
        time.sleep(time_to_sleep)


if __name__ == "__main__":
    main()
