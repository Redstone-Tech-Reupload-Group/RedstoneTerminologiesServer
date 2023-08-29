import os.path
import pandas as pd


def add_word(word, trans, desc, example, tag, repo_path):
    first_char = word[0].upper()
    dict_path = os.path.join(repo_path, f'dictionary/{first_char}.csv')

    if not os.path.exists(dict_path):
        dictionary = pd.DataFrame(columns=['Word', 'Translation', 'Description', 'Example', 'Tag'])
    else:
        dictionary = pd.read_csv(dict_path, index_col=0, encoding='utf-8')

    record = pd.DataFrame.from_dict({
        'Word': [word],
        'Translation': [trans],
        'Description': [desc],
        'Example': [example],
        'Tag': ['|'.join(tag)]
    })

    dictionary = pd.concat([dictionary, record], ignore_index=True)
    dictionary.to_csv(dict_path, encoding='utf-8')

    index = dictionary.index[-1]

    add_index(word, tag, index, repo_path)

    return index


def add_index(word, tag, index, repo_path):
    index_path = os.path.join(repo_path, 'index.csv')

    if not os.path.exists(index_path):
        index_data = pd.DataFrame(columns=['Word', 'Tag', 'Index', 'FirstChar'])
    else:
        index_data = pd.read_csv(index_path)

    record = pd.DataFrame.from_dict({
        'Word': [word],
        'Tag': ['|'.join(tag)],
        'Index': [index],
        'FirstChar': [word[0].upper()]
    })

    index_data = pd.concat([index_data, record], ignore_index=True)
    index_data = index_data.sort_values(by='Word')
    index_data.to_csv(index_path, index=False, encoding='utf-8')

    print(index_data)

    return len(index_data) - 1
