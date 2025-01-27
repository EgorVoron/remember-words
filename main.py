from random import shuffle
import json
import os
import datetime
import sys

from websites_utils import get_ligvolive_page
from utils import get_variants, cut, reverse_dict

language = sys.argv[1] if len(sys.argv) > 1 else 'latin'
website = sys.argv[2] if len(sys.argv) > 2 else 'lingvolive'

"""
from = foreign -> native
to = native -> foreign
"""
command_to_dict_path: dict[str, str] = {}
for dictionary_filename in os.listdir(f'dictionaries/{language}'):
    file_path = os.path.join(f'dictionaries/{language}', dictionary_filename)
    if not os.path.isfile(file_path):
        continue
    dictionary_name = dictionary_filename.split('.json')[0]
    command_to_dict_path[dictionary_name + '_from'] = file_path
    command_to_dict_path[dictionary_name + '_to'] = file_path

words_num = None
command = input(f'choose dictionary from {list(command_to_dict_path.keys())}: ')
if '/' in command:
    command, _, words_num = command.partition('/')
command_type = command.rpartition('_')[2]

with open(command_to_dict_path[command], 'r+') as dictionary_file:
    dictionary_json = json.load(dictionary_file)
    if command_type == "to":
        dictionary_json = reverse_dict(dictionary_json)

use_website = int(input(f'do you want me to use {website}.com data? 1/0 '))
if use_website:
    with open(f'dictionaries/{language}/websites_dictionaries/{website}.json', 'r+') as wf:
        website_dict = json.load(wf)

chosen_dict_items = list(dictionary_json.items())
shuffle(chosen_dict_items)

words_num = int(words_num) if words_num else len(chosen_dict_items)
r = 0
errors: dict[str, str] = {}
for idx, words_pair in enumerate(chosen_dict_items[:words_num]):
    source_word, target_word = words_pair
    user_input = input(f'{source_word}: ')
    user_was_right = user_input in get_variants(target_word)
    if user_was_right:
        r += 1
        print(f'right! ✅. additional info: {target_word}')
    else:
        print(f'wrong ❌. additional info: {target_word}')
    if use_website:
        if command_type == "from":
            cut_word = cut(source_word)
        else:
            cut_word = cut(target_word)
        print(get_ligvolive_page(cut_word))
        print(f'{website} info:', website_dict.get(cut_word, ''))
    if not user_was_right:
        mistype = input('if you were right but mistyped please type "1": ')
        if mistype == "1":
            r += 1
        else:
            errors.update({source_word: target_word})
    print(f'current score: {r}/{idx + 1}')
    print('-' * 20)
print('=' * 20)
print(f'remember this words: {errors}')

with open(f'scores/{language}/{command}.txt', 'a') as scores_file:
    scores_file.write(f'{datetime.datetime.now()}, {r}/{words_num}\n')
