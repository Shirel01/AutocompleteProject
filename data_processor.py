import os
import string
import sentence_trie


def clean_text(text):
    """Clean the text by converting to lowercase, removing punctuation, and extra spaces."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = ' '.join(text.split())  # Remove extra spaces
    return text.strip()


def build_trie_from_files(directory, sentence_trie):
    """
    Read files from directory, clean text, and insert sentences into a trie.

    Args:
        directory (str): Path to the directory containing text files.
        sentence_trie (SentenceTrie): Instance of SentenceTrie to insert sentences into.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        cleaned_sentence = clean_text(line)
                        sentence_trie.add_sentence(cleaned_sentence)


if __name__ == "__main__":
    sentenceTrie = sentence_trie.SentenceTrie()
    directory_path = "/path/to/your/directory"
    build_trie_from_files(directory_path, sentenceTrie)

