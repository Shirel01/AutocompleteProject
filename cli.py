import argparse
import os
import re
import string
import sys
from typing import List, Union
from sentence_trie import SentenceTrie
from word_trie import WordTrie


PATTERN = r'[^a-zA-Z0-9\s]'


def clean_text(text):
    """Clean the text by converting to lowercase, removing punctuation, and extra spaces."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = ' '.join(text.split())  # Remove extra spaces
    return text.strip()


def input_validation(string: str) -> Union[str, None]:
    """
    Validate the user input.
    :param string: the user input.
    :return: the user input after validation.
    """
    clean_line = re.sub(PATTERN, '', string).lower().strip()
    if clean_line == '' or clean_line == '\n' or clean_line == ' ':
        print("You didn't enter a text.")
        return None
    else:
        return clean_line


def user_input():
    """
    Get the user input.
    :return: the user input.
    """
    string = input("Enter your text: ")
    return string


def build_tries_from_files(directory, sentence_trie, word_trie):
    """
    Read files from directory, clean text, and insert sentences into a trie. Then from the sentence trie build the word Trie.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)  # Only the filename without the path
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        cleaned_sentence = clean_text(line)
                        sentence_trie.add_sentence(cleaned_sentence, file_name)
    word_trie.insert_data(sentence_trie)


def init_db(path_to_data: str) -> (WordTrie, SentenceTrie):
    """
    Initialize the database with the data from the files and return the word trie and the sentence trie.
    :return: word trie, sentence trie.
    """
    sentence_trie = SentenceTrie()
    word_trie = WordTrie()
    build_tries_from_files(path_to_data, sentence_trie, word_trie)
    return word_trie, sentence_trie


def init(path_to_data: str):
    """
    Initialize the search engine and return the word trie and the sentence trie.
    :return: word trie, sentence trie.
    """
    print("Welcome to the search engine!")
    print("Loading the database...")
    word_trie, sentence_trie = init_db(path_to_data)
    print("The search engine is ready to use!")
    return word_trie, sentence_trie


def main():
    parser = argparse.ArgumentParser(description="CLI interface for the project.")
    parser.add_argument("directory", type=str, help="Path to the directory containing text files")
    args = parser.parse_args()

    word_trie, sentence_trie = init(args.directory)
    print("This is a search engine for auto-complete sentences.")
    print("Enter your text and get the best 5 auto-complete sentences.")
    print("Don't worry about spelling mistakes or lower/upper case, we will take care of it.")
    print("Enter 'exit' to exit the program.")

    while True:
        string = user_input()
        string = input_validation(string)
        if string is None:
            continue
        if string == "exit":
            break
        else:
            results = sentence_trie.search_sentence_prefix(word_trie, string)
            for sentence, source in results:
                print(f"Complete Sentence: {sentence}, Source: {source}")



if __name__ == "__main__":
    main()
