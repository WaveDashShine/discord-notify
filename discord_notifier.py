import time
import random
import asyncio
import discord
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from configs import DISCORD_TOKEN, DISCORD_CHANNEL_ID, MANHWA_CONFIG
from debug.debug_log import logger
from manhwa_checker.main import get_manhwa_updates
from manhwa_checker.timer import Timer, get_timedelta_from_str
from datetime import datetime
from manhwa_checker.pages.asura import Chapter


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


def wait_for_next_poll_time():
    polling_rate_seconds = get_timedelta_from_str(
        MANHWA_CONFIG.asura.interval
    ).total_seconds()
    time_to_sleep: int = random.randrange(
        start=int(polling_rate_seconds * 0.9), stop=int(polling_rate_seconds * 1.1)
    )
    logger.info(f"sleeping for {time_to_sleep} seconds")
    time.sleep(time_to_sleep)


def main():
    timer = Timer()  # instantiate based on log time
    locked_chapters: list[Chapter] = []
    has_error = False
    while True:
        logger.info(f"Checking at {datetime.now()}")
        try:
            available_chapters: list[Chapter] = get_manhwa_updates(
                timer=timer, locked_chapters=locked_chapters
            )
            if locked_chapters:
                logger.info(f"Locked chapters: {locked_chapters}")
            if available_chapters:
                logger.info(f"New chapters: {available_chapters}")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(send_message(available_chapters))
        except PlaywrightTimeoutError as e:
            logger.error(e)
            has_error = True
        if not has_error:
            timer = Timer()
        wait_for_next_poll_time()


if __name__ == "__main__":
    main()
