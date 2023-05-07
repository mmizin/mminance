from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os

from config import FilePaths, Color


def print_result(words):
    res = ''

    for count, item in enumerate(words, start=1):
        res += item + ' '
        if not count % 7:
            res += '\n'

    print(f'{Color.GREEN.value}{res}{Color.END.value}')


def read_data_from_the_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    return text


def find_all_words_with_exact_length(length):
    pattern = rf'\b\w{{{length}}}\b'
    text = read_data_from_the_file(FilePaths.WORD_OF_THE_DAY_DATA.path)
    match = list(set(re.findall(pattern, text, flags=re.IGNORECASE)))

    return match


def find_matched_words(letters_in_word, words):
    matched_words = []

    random_letters_in = letters_in_word['include']['random']
    letters_with_index = letters_in_word['include']["with_index"]
    repeated_letters = letters_in_word['include']["repeated"]
    letters_to_exclude = letters_in_word['exclude']

    for word in words:
        matched = True
        for k, v in letters_with_index.items():
            if word[k-1] != v:
                matched = False
                break
        if matched:
            for letter in random_letters_in:
                if letter not in word:
                    matched = False
                    break
        if matched:
            for k, v in repeated_letters.items():
                if word.count(v) != k:
                    matched = False
                    break
        if matched:
            for letter in letters_to_exclude:
                if letter in word:
                    matched = False
                    break
        if matched:
            matched_words.append(word)

    return matched_words


def prepare_data(urls):
    for url in urls:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        with open(FilePaths.WORD_OF_THE_DAY_DATA.path, 'a+') as file:
            file.write(text)


def prepare_letters_to_find(l_include, l_exclude):
    letters = {"include": {"random": [], "with_index": {}, "repeated": {}},
               "exclude": []}

    for letter in l_include:
        if len(letter) == 1:
            letters["include"]['random'].append(letter)
        elif len(letter) == 2:
            letters["include"]['repeated'][int(letter[-1])] = letter[0]
        else:
            letters["include"]['with_index'][int(letter[0])] = letter[-1]

    letters["exclude"] = l_exclude

    return letters


def check_word_was_found(words):
    print(f"\n{Color.YELLOW.value}Here are the words that we found for you:{Color.END.value}")
    print_result(words)
    find = input(f"{Color.YELLOW.value}If the word was matched enter Y else N :=> {Color.END.value}")
    find = True if find.lower() == 'y' else False
    if find:
        print(f'{Color.CYAN.value}Awesome, it was a pleasure to work for you.{Color.END.value}')
        clear_file(FilePaths.WORD_OF_THE_DAY_DATA.path)
        exit()


def clear_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


if __name__ == '__main__':
    input_urls = input(f"{Color.YELLOW.value}Enter URLs separated by space :=> {Color.END.value}").split()
    prepare_data(input_urls)
    word_length = int(input(f"\n{Color.YELLOW.value}Data was generated. Enter the word length :=> {Color.END.value}"))
    words_filtered_by_length = find_all_words_with_exact_length(word_length)
    check_word_was_found(words_filtered_by_length)

    while True:
        letters_in = input(f"\n{Color.YELLOW.value}Enter matching letters separated by space. "
                           f"\nIf you know letter position pass it like that 3=a b 4=c\n"
                           f"if the letter is repeated pass it like that a3 :=> {Color.END.value}").split()
        letters_not_in = input(f"\n{Color.YELLOW.value}Enter letters that should be excluded :=> {Color.END.value}").split()
        letters_to_find = prepare_letters_to_find(letters_in, letters_not_in)
        matched_words = find_matched_words(letters_to_find, words_filtered_by_length)
        check_word_was_found(matched_words)
        print(f"{Color.BOLD.value}{Color.GREEN.value}Try to check another word 🤞{Color.END.value}")
