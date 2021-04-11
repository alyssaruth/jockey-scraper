from utils import get_game_pages

if __name__ == '__main__':
    pages = get_game_pages()

    results_table_str = '{| class="article-table sortable"\n|+Chan Indices\n!Game' \
                        '\n! data-sort-type="number" | Rounds\n! data-sort-type="number" | Chan Index' \
                        '\n! data-sort-type="number" | Ratio\n'

    for page in pages:
        results_table_str += f'|-\n|{page.as_wiki_link()}\n|{page.rounds}\n|{page.chan_index}\n|{page.get_chan_ratio()}\n'

    results_table_str += '|}'
    print(results_table_str)
