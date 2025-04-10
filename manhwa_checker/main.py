from playwright.sync_api import sync_playwright
from debug.debug_log import logger
from configs import MANHWA_CONFIG
from manhwa_checker.pages.asura import AsuraPage, Chapter
from manhwa_checker.timer import Timer
from datetime import timedelta

IS_DEBUG = False


def get_manhwa_updates(timer: Timer, locked_chapters: list[Chapter]) -> list[Chapter]:
    latest_chapters: list[Chapter] = get_latest_chapters()
    available_chapters = []
    for chapter in latest_chapters:
        if chapter.is_locked:
            if chapter not in locked_chapters:
                locked_chapters.append(chapter)
            continue
        if timer.is_new_since_start_time(time_string=chapter.time_available):
            available_chapters.append(chapter)
        elif chapter in locked_chapters:
            available_chapters.append(chapter)
            locked_chapters.remove(chapter)
    return available_chapters


def get_latest_chapters() -> list[Chapter]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not IS_DEBUG)
        context = browser.new_context()
        page = context.new_page()
        asura = AsuraPage(page=page)
        page.goto(MANHWA_CONFIG.asura.url)
        latest_chapters = asura.get_latest_chapters()
        browser.close()
    return latest_chapters


def main():
    timer = Timer(rewind=timedelta(hours=23))
    locked_chapters: list[Chapter] = []
    chapter_list = get_manhwa_updates(timer=timer, locked_chapters=locked_chapters)
    for chapter in chapter_list:
        logger.info(f"{chapter}")


if __name__ == "__main__":
    IS_DEBUG = True
    main()
