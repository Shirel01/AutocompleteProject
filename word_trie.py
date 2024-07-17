import sentence_trie
from sentence_trie import WordNode


class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        self.char = char
        self.is_end_of_word = False
        # A counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0
        # A dictionary of child nodes
        # Keys are characters, values are nodes
        self.children = {}
        # Array of references of words in SentenceTrie
        self.sentenceTrieRef = []


class WordTrie:

    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word_node: WordNode):
        """Insert a word into the trie"""
        node = self.root
        word = word_node.word
        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                newNode = TrieNode(char)
                node.children[char] = newNode
                node = newNode

        node.is_end_of_word = True
        # Increment the counter to indicate that we see this word once more
        node.counter += 1
        node.sentenceTrieRef.append(word_node)



