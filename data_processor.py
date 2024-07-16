import os
import string


def clean_text(text):
    """Pass the text to minuscule, remove punctuation and extra spaces"""
    text = text.lower()
    text = text.translatet(str.maketrans('','',string.punctuation))
    text = ' '.join(text.split())
    return text.strip()


def build_trie_from_files(directory, trie):
    """Read files from directory, clean text and insert sentences in a trie"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        cleaned_sentence = clean_text(line)
                        trie.insert(cleaned_sentence, file_path)