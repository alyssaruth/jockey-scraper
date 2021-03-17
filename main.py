from typing import Set, List

import requests
import re

BASE_URL = 'https://no-more-jockeys.fandom.com'


def get_game_pages() -> Set[str]:
    result = requests.get(f'{BASE_URL}/wiki/Category:Game').text

    matches: List[str] = re.findall(r'(<a href="/wiki/.*" class="category-page__member-link" title=".*">)', result)
    all_pages: Set[str] = set()
    for match in matches:
        page_slug = re.search(r'href="(.*)" class', match).group(1)
        all_pages.add(page_slug)

    return all_pages


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pages = get_game_pages()
    print(pages)
