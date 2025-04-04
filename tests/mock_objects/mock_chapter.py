from manhwa_checker.pages.asura import Chapter


class MockChapter(Chapter):
    def __init__(self, title: str, number: str, time_available: str):
        self.number = number
        self.time_available = time_available
        super().__init__(title=title, locator=None)

    def _get_chapter_number(self) -> str:
        return self.number

    def _get_time_available(self) -> str:
        return self.time_available

    def _get_link(self):
        return f"www.{self}.com"
