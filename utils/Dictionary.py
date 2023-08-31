# -*- coding: utf-8 -*-

import json
import os.path
import pandas as pd

import Config


def add_word(word, trans, desc, example, tag, repo_path=Config.REPO_PATH):
    first_char = word[0].upper()
    dict_path = os.path.join(repo_path, f'dictionary/{first_char}.csv')

    if not os.path.exists(dict_path):
        dictionary = pd.DataFrame(columns=['Word', 'Translation', 'Description', 'Example', 'Tag'])
    else:
        dictionary = pd.read_csv(dict_path, index_col=0, encoding='utf-8')

        if word in dictionary['Word'].values:
            return '', -1

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

    add_index(word, tag, index)
    modify_tag(tag, first_char, index)

    return first_char, index


def search_word(word, repo_path=Config.REPO_PATH):
    index_path = os.path.join(repo_path, 'index.csv')

    if not os.path.exists(index_path):
        return -1, {}

    index_df = pd.read_csv(index_path, encoding='utf-8')

    if word not in index_df['Word'].values:
        return -1, {}
    else:
        index_data = index_df.loc[index_df['Word'] == word]
        fist_char = index_data['FirstChar'][0]
        index = index_data['Index'][0]
        dict_path = os.path.join(repo_path, f'dictionary/{fist_char}.csv')

        dict_data = pd.read_csv(dict_path, encoding='utf-8', index_col=0)

        return index, dict_data.iloc[index].to_dict()


def modify_word(index, word, trans, desc, example, tag, repo_path=Config.REPO_PATH):
    dict_path = os.path.join(repo_path, f'dictionary/{word[0].upper()}.csv')

    if not os.path.exists(dict_path):
        return -1

    dict_data = pd.read_csv(dict_path, encoding='utf-8', index_col=0)
    dict_data.at[index, 'Translation'] = trans
    dict_data.at[index, 'Description'] = desc
    dict_data.at[index, 'Example'] = example
    dict_data.at[index, 'Tag'] = '|'.join(tag)

    dict_data.to_csv(dict_path, encoding='utf-8')

    return 1


def add_index(word, tag, index, repo_path=Config.REPO_PATH):
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

    return len(index_data) - 1


def get_tag(repo_path=Config.REPO_PATH):
    tag_path = os.path.join(repo_path, 'tag.json')

    if not os.path.exists(tag_path):
        return []
    else:
        with open(tag_path, 'r', encoding='utf-8') as tag_file:
            tag_str = tag_file.read()

        tag_dict = json.loads(tag_str)
        return list(tag_dict)


def add_tag(tag, repo_path=Config.REPO_PATH):
    tag_path = os.path.join(repo_path, 'tag.json')

    if not os.path.exists(tag_path):
        tag_dict = {}
    else:
        with open(tag_path, 'r', encoding='utf-8') as tag_file:
            tag_dict = json.load(tag_file)

    if tag in tag_dict:
        return -1, list(tag_dict)
    else:
        tag_dict[tag] = []

        with open(tag_path, 'w', encoding='utf-8') as tag_file:
            json.dump(tag_dict, tag_file, ensure_ascii=False)
        return 1, list(tag_dict)


def modify_tag(tags, first_char, index, repo_path=Config.REPO_PATH):
    tag_path = os.path.join(repo_path, 'tag.json')
    with open(tag_path, 'r', encoding='utf-8') as tag_file:
        tag_dict = json.load(tag_file)

    for tag in tags:
        tag_dict[tag].append(f'{first_char}-{index}')

    with open(tag_path, 'w', encoding='utf-8') as tag_file:
        json.dump(tag_dict, tag_file, ensure_ascii=False)
