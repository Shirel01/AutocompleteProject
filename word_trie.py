import sentence_trie
from sentence_trie import WordNode
import typing
from dataclasses import dataclass
import typing


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

    def insert_data(self, sentence_trie: sentence_trie.SentenceTrie):
        """ Insert all the words from sentence trie to wordTrie"""
        word_nodes = sentence_trie.find_all_nodes(sentence_trie.root)
        for wordNode in word_nodes:
            self.insert(wordNode)

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


    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end_of_word:
            self.output.append((prefix + node.char, node.counter, node.sentenceTrieRef))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def search_prefix(self, prefix: str):
        """Given a prefix if find it, return all words with this prefix  sort the words by the number of
        times they have been inserted"""
        self.output = []
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        self.dfs(node, prefix[:-1])
        return sorted(self.output, key=lambda prefix: prefix[1], reverse=True)  # sorted according to counter



