from utils import get_game_pages, count_where

if __name__ == '__main__':
    pages = get_game_pages()

    success_count = count_where(lambda game: game.chan_index == '∞', pages)
    total_count = len(pages)
    all_ratios = [page.get_raw_chan_ratio() for page in pages]
    overall_ratio = sum(all_ratios)/total_count
    formatted_ratio = '{:.1%}'.format(overall_ratio)

    page_str = f'In total, the Chan Index has been recorded for \'\'\'{total_count}\'\'\' games. ' \
               f'On average, Jackie Chan is a valid move for the first \'\'\'{formatted_ratio}\'\'\' of a given game.\n' \
               f'There have been \'\'\'{success_count}\'\'\' games where the Chan Index was ∞.\n'

    results_table_str = '{| class="article-table sortable"\n|+Chan Indices\n!Game' \
                        '\n! data-sort-type="number" | Rounds\n! data-sort-type="number" | Chan Index' \
                        '\n! data-sort-type="number" | Ratio\n'

    for page in pages:
        results_table_str += f'|-\n|{page.as_wiki_link()}\n|{page.rounds}\n|{page.chan_index}\n|{page.get_chan_ratio()}\n'

    results_table_str += '|}'
    print(page_str)
    print(results_table_str)
