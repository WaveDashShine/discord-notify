import pytest
import manhwa_checker.main
from manhwa_checker.pages.asura import Chapter
from manhwa_checker.timer import Timer
from datetime import timedelta
from mock_objects.mock_chapter import MockChapter

NEW_CHAPTER = MockChapter(title="New Chapter", number="1", time_available="6 hours ago")
OLD_CHAPTER = MockChapter(title="old chapter", number="3", time_available="3 days ago")
LOCKED_CHAPTER = MockChapter(
    title="Locked Chapter", number="2", time_available="Public in 3 hours"
)
CHAPTER_LIST = [NEW_CHAPTER, LOCKED_CHAPTER, OLD_CHAPTER]


class TestManhwaUpdates:
    @pytest.fixture(scope="class")
    def timer(self):
        """
        timer set to 1 day ago
        """
        timer = Timer(rewind=timedelta(days=1))
        yield timer

    @pytest.fixture(scope="function", autouse=True)
    def patched(self, monkeypatch):
        def get_mock_chapter_list():
            return CHAPTER_LIST

        monkeypatch.setattr(
            manhwa_checker.main,
            manhwa_checker.main.get_latest_chapters.__name__,
            get_mock_chapter_list,
        )

    def test_get_new_chapters(self, timer):
        chapter_list = manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=[]
        )
        assert NEW_CHAPTER in chapter_list

    def test_old_chapters_are_not_considered_new(self, timer):
        chapter_list = manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=[]
        )
        assert OLD_CHAPTER not in chapter_list

    def test_locked_chapters_are_not_considered_new(self, timer):
        chapter_list = manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=[]
        )
        assert LOCKED_CHAPTER not in chapter_list

    def test_locked_chapters_saved_for_later(self, timer):
        locked_chapters: list[Chapter] = []
        manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        assert LOCKED_CHAPTER in locked_chapters

    def test_new_chapters_not_saved_for_later(self, timer):
        locked_chapters: list[Chapter] = []
        manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        assert NEW_CHAPTER not in locked_chapters

    def test_old_chapters_not_saved_for_later(self, timer):
        locked_chapters: list[Chapter] = []
        manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        assert OLD_CHAPTER not in locked_chapters

    def test_locked_chapters_removed_after_becoming_available(self, timer, monkeypatch):
        """
        assumes that after the chapter is unlocked after 6 hours,
         the time available will display: 'available 6 hours ago'
         - considered an old chapter - but since it was locked, needs to be treated as new chapter
        """
        previously_locked_chapter = MockChapter(
            title=OLD_CHAPTER.title,
            number=OLD_CHAPTER.number,
            time_available="public in 5 hours",
        )
        locked_chapters: list[Chapter] = [previously_locked_chapter]
        manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        assert previously_locked_chapter not in locked_chapters

    def test_locked_chapters_are_treated_as_new_after_becoming_available(
        self, timer, monkeypatch
    ):
        """
        assumes that after the chapter is unlocked after 6 hours,
         the time available will display: 'available 6 hours ago'
         - considered an old chapter - but since it was locked, needs to be treated as new chapter
        """
        previously_locked_chapter = MockChapter(
            title=OLD_CHAPTER.title,
            number=OLD_CHAPTER.number,
            time_available="public in 5 hours",
        )
        locked_chapters: list[Chapter] = [previously_locked_chapter]
        chapter_list = manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        assert OLD_CHAPTER in chapter_list

    def test_locked_chapters_not_added_again(self, timer):
        """
        locked chapters shouldn't be added more than once
        """
        locked_chapters: list[Chapter] = []
        manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        manhwa_checker.main.get_manhwa_updates(
            timer=timer, locked_chapters=locked_chapters
        )
        locked_chapter = [c for c in locked_chapters if c == LOCKED_CHAPTER]
        assert len(locked_chapter) == 1
