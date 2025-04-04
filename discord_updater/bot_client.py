import time

import discord
from configs import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from debug.debug_log import logger
from manhwa_checker.main import get_manhwa_updates
from manhwa_checker.timer import Timer
from datetime import timedelta
from manhwa_checker.pages.asura import Chapter
import random


POLLING_RATE = 60  # minutes


class MyClient(discord.Client):
    async def on_ready(self):
        logger.info(f"Logged on as {self.user}!")
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        logger.info(f"Channel: {channel}")
        timer = Timer(rewind=timedelta(days=1))
        locked_chapters: list[Chapter] = []
        while True:
            chapter_list: list[Chapter] = get_manhwa_updates(
                timer=timer, locked_chapters=locked_chapters
            )
            for chapter in chapter_list:
                await channel.send(f"{chapter}\n{chapter.link}")
            timer = Timer()
            elapsed_seconds = 60 * POLLING_RATE
            time.sleep(
                random.randrange(
                    start=int(elapsed_seconds * 0.9), stop=int(elapsed_seconds * 1.1)
                )
            )

    async def on_message(self, message):
        logger.info(f"Message | {message.author}: {message.content}")


def main():
    """
    # Message Intent: required for sending and receiving messages
    - set in Discord API portal
    """
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
