from operator import index

from playwright.sync_api import Page, Locator
from configs import MANHWA_CONFIG


class Chapter:
    def __init__(self, title: str, locator: Locator):
        """
        use inner_text because it keeps the \n\n spacing
        """
        self.locator = locator
        self.timeout = 1000
        self._splitter = "\n\n"

        self.title: str = title
        self.number: str = self._get_chapter_number()
        self.time_available: str = self._get_time_available()
        self.is_locked: bool = "public" in self.time_available.lower()
        self.link = self._get_link()

    def __str__(self):
        return f"{self.title}: Chapter {self.number} - {self.time_available}"

    def __repr__(self):
        # printing list
        return f"\n\t{str(self)}"

    def __eq__(self, other):
        if not isinstance(other, Chapter):
            return NotImplemented
        return self.title == other.title and self.number == other.number

    def _get_link(self):
        return f'{MANHWA_CONFIG.asura.url}{(
            self.locator.locator("a", has_text="chapter")
            .filter(visible=True)
            .first.get_attribute("href", timeout=self.timeout)
        )}'

    def _get_chapter_number(self) -> str:
        chapter_text = self.locator.inner_text(timeout=self.timeout).split(
            self._splitter
        )[0]
        chapter_number = "".join([c for c in chapter_text if c.isdigit()])
        return chapter_number

    def _get_time_available(self) -> str:
        return self.locator.inner_text(timeout=self.timeout).split(self._splitter)[-1]


class UpdateCard:
    def __init__(self, title: str, locator: Locator):
        self.locator = locator
        self.title = locator.get_by_text(title).text_content()
        self.chapter_list: list[Chapter] = []
        self._init_chapter_list()

    def _init_chapter_list(self):
        chapter_locator_list = (
            self.locator.locator("span", has_text="chapter")
            .filter(visible=True, has=self.locator.page.locator("a"))
            .all()
        )
        for chapter_locator in chapter_locator_list:
            chapter = Chapter(title=self.title, locator=chapter_locator)
            self.chapter_list.append(chapter)


class AsuraPage:

    def __init__(self, page: Page):
        self.page = page

    def wait_for_load(self):
        self.page.wait_for_load_state(state="load")

    def latest_update_card(self, title: str) -> UpdateCard | None:
        chapter = self.page.locator("text=chapter >> visible=true")
        upper_limit_chapter = chapter.nth(2)
        not_displayed_chapter = chapter.nth(3)
        update_card_locator = (
            self.page.locator(".grid")
            .filter(has=self.page.get_by_text(text=title))
            .filter(
                has=upper_limit_chapter,
                has_not=not_displayed_chapter,
            )
        )
        if update_card_locator.is_visible():
            return UpdateCard(title=title, locator=update_card_locator)
        else:
            return None

    def get_latest_chapters(self) -> list[Chapter]:
        self.wait_for_load()
        latest_chapter_list = []
        for title in MANHWA_CONFIG.asura.titles:
            update_card = self.latest_update_card(title=title)
            if update_card:
                for chapter in update_card.chapter_list:
                    latest_chapter_list.append(chapter)
        return latest_chapter_list
