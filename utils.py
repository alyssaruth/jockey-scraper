import re
from datetime import datetime
from typing import Set, List, Callable, Iterable, TypeVar

import requests

BASE_URL = 'https://no-more-jockeys.fandom.com'


class GamePage(object):
    slug: str
    full_url: str
    name: str
    recorded_date: datetime
    chan_index: str
    raw_plays_table: str
    rounds: int

    def __init__(self, slug: str):
        self.slug = slug
        self.full_url = f'{BASE_URL}/wiki/{slug}'
        self.name = slug.replace('_', ' ').replace('%27', '\'')

        contents = requests.get(self.full_url).text.replace('\n', '')
        self.recorded_date = get_recorded_date(contents)
        self.chan_index = get_chan_index(contents)
        self.raw_plays_table = re.search(r'<tbody>(.*)</tbody>', contents).group(1)
        self.rounds = get_rounds(contents)

    def as_wiki_link(self) -> str:
        return f'[[{self.name}|{self.name}]]'

    def get_normalised_chan_index(self) -> int:
        if self.chan_index == '∞':
            return self.rounds

        return int(self.chan_index)

    def get_raw_chan_ratio(self) -> float:
        return self.get_normalised_chan_index() / self.rounds

    def get_chan_ratio(self) -> str:
        raw_ratio = self.get_normalised_chan_index() / self.rounds
        return '{:.1%}'.format(raw_ratio)

    def __str__(self):
        return self.name


def get_game_pages() -> List[GamePage]:
    result = requests.get(f'{BASE_URL}').text

    matches: List[str] = re.findall(r'(<td><a href="/wiki/(.*)" title=".*">)', result)
    all_pages: Set[GamePage] = set()
    for match in matches:
        page_slug = match[1]
        all_pages.add(GamePage(page_slug))

    return sorted(all_pages, key=lambda page: page.recorded_date)


def get_page_contents(page_name: str) -> str:
    return requests.get(f'{BASE_URL}/wiki/{page_name}').text.replace('\n', '')


def get_recorded_date(page_contents: str) -> datetime:
    recorded_str = re.search(
        r'<h3 class="pi-data-label pi-secondary-font">Recorded</h3>		<div class="pi-data-value pi-font">([0-9/]+)</div>',
        page_contents).group(1)
    return datetime.strptime(recorded_str, "%d/%m/%Y")


def get_chan_index(page_contents: str) -> str:
    chan_result = re.search(
        r'<a href="/wiki/Chan_Index" title="Chan Index">Chan index</a></h3>		<div class="pi-data-value pi-font">([0-9∞]+).*</div>',
        page_contents)

    if chan_result is None:
        return ''

    return chan_result.group(1)


def get_rounds(page_contents: str) -> int:
    rounds_result = re.search(
        r'<h3 class="pi-data-label pi-secondary-font">Rounds</h3>		<div class="pi-data-value pi-font">([0-9]+)</div>',
        page_contents)
    return int(rounds_result.group(1))


T = TypeVar('T')


def count_where(fn: Callable[[T], bool], iterable: Iterable[T]) -> int:
    return len(list(filter(fn, iterable)))
