

class WordNode:
    def __init__(self, word, father, children=None):
        self.word = word
        self.father = father
        self.children = children or []


class SentenceTrie:
    def __init__(self):
        self.root = WordNode(None, None)

    def add_sentence(self, sentence: str) -> None:
        """
        Adds a sentence to the trie
        :param sentence: str
        :return: None
        """
        words = sentence.split()
        node = self.root
        for word in words:
            node = self.add_word(word, node)

    def add_word(self, word: str, father: WordNode) -> WordNode:
        """
        Adds a word to the trie, called only by add_sentence
        :param word: the current word in the sentence
        :param father: the father node of the current word
        :return: the node of the current word
        """
        for child in father.children:
            if child.word == word:
                return child
        node = WordNode(word, father) #create a new node with the word that we have added
        father.children.append(node) #add this children to the father
        return node


    def traverse(self, node=None, words=None):
        """
        Traverse the SentenceTrie to collect all words.
        :param node: current node
        :param words: list of words
        :return: list of words
        """
        if node is None:
            node = self.root
        if words is None:
            words = []
        if node.word:
            words.append(node.word)
        for child in node.children:
            self.traverse(child, words)
        return words
