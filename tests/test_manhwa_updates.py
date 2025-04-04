import pytest
from manhwa_checker.pages.asura import AsuraPage
import manhwa_checker.main
from manhwa_checker.pages.asura import AsuraPage, Chapter
from manhwa_checker.timer import Timer
from datetime import timedelta
from mock_objects.mock_chapter import MockChapter


class TestManhwaUpdates:
    # TODO: how to mock asura's return functions here
    # TODO: mock chapter init here override with TestChapter inherit
    def test_locked_chapters_saved_for_later(self, monkeypatch):
        """
        locked chapters are accumulated for later
        """

        def test_chapter_list():
            # TODO: locked chapter list
            return []

        timer = Timer()
        locked_chapters: list[Chapter] = []
        monkeypatch.setattr(
            manhwa_checker.main,
            manhwa_checker.main.get_latest_chapters.__name__,
            test_chapter_list,
        )
        chapter_list = manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        assert not chapter_list

    def test_locked_chapters_removed_after_available(self, monkeypatch):
        # requires chapters inside locked chapter list, remove after
        # also assert in available chapters returned
        pass

    def test_available_chapters(self, monkeypatch):
        pass  # simple test requires some available chapters
