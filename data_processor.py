import os
import string
import sentence_trie
import word_trie


def clean_text(text):
    """Clean the text by converting to lowercase, removing punctuation, and extra spaces."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = ' '.join(text.split())  # Remove extra spaces
    return text.strip()


def build_trie_from_files(directory, sentence_trie, word_trie):
    """
    Read files from directory, clean text, and insert sentences into a trie. Then from the sentence trie build the word Trie.

    Args:
        directory (str): Path to the directory containing text files.
        sentence_trie (SentenceTrie): Instance of SentenceTrie to insert sentences into.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        cleaned_sentence = clean_text(line)
                        sentence_trie.add_sentence(cleaned_sentence)
    # Traverse SentenceTrie and add words to WordTrie
    words = sentence_trie.traverse()
    for word in words:
        word_trie.insert(word)


if __name__ == "__main__":
    sentenceTrie = sentence_trie.SentenceTrie()
    word_trie = word_trie.WordTrie()
    directory_path = "C:/Users/shire/Downloads/Archive2"
    build_trie_from_files(directory_path, sentenceTrie, word_trie)

