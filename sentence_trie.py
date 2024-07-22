import typing
class WordNode:
    def __init__(self, word, father, sources=None, children=None):
        self.word = word
        self.father = father
        self.sources = sources or []     #add field source
        self.children = children or []



class SentenceTrie:
    def __init__(self):
        self.root = WordNode(None, None)

    def add_sentence(self, sentence: str, source_file:str) -> None:
        """
        Adds a sentence to the trie
        :param sentence: str
        :return: None
        """
        words = sentence.split()
        node = self.root
        for word in words:
            node = self.add_word(word, node, source_file)

    def add_word(self, word: str, father: WordNode, source_file: str) -> WordNode:
        """
        Adds a word to the trie, called only by add_sentence
        :param word: the current word in the sentence
        :param father: the father node of the current word
        :return: the node of the current word
        """
        for child in father.children:
            if child.word == word:
                if source_file not in child.sources:
                    child.sources.append(source_file)

                return child
        node = WordNode(word, father, [source_file])  # create a new node with the word that we have added
        father.children.append(node)  # add this children to the father
        return node

    def find_all_nodes(self, root: WordNode) -> typing.List[WordNode]:
        """
        Finds all the nodes of a node, called when there is a need to build words_trie
        :param root: root node of the sentence trie
        :return: a list of all the nodes
        according to dfs
        """
        nodes = []
        stack = [root]

        while stack:
            current_node = stack.pop()
            if current_node.word:
                nodes.append(current_node)
            stack.extend(current_node.children)

        return nodes

    def reconstruct_sentence(self, node: WordNode) -> typing.Tuple[typing.List[str], str]:
        words = []
        original_node = node
        while node.father is not None:
            if node.word is not None:
                words.append(node.word)
            node = node.father
        words.reverse()

        def complete_sentence_iterative(start_node: WordNode, initial_sentence: typing.List[str]) -> typing.List[str]:
            stack = [(start_node, initial_sentence)]
            sentences = []

            while stack:
                current_node, current_sentence = stack.pop()
                if not current_node.children:
                    sentences.append(' '.join(current_sentence))
                else:
                    for child in current_node.children:
                        stack.append((child, current_sentence + [child.word]))

            return sentences

        initial_sentence = words[:]
        # Start completing the sentence from the original node where prefix ends
        complete_sentences = complete_sentence_iterative(original_node, initial_sentence)
        return complete_sentences, original_node.sources
