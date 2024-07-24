import typing
import word_trie
from word_trie import AutoCompleteData
#from AutocompleteProject.word_trie import WordTrie
#from AutocompleteProject.word_trie import AutoCompleteData

class WordNode:
    def __init__(self, word, father, sources=None, children=None):
        self.word = word
        self.father = father
        self.sources = sources or []  # add field source
        self.children = children or []





class SentenceTrie:
    def __init__(self):
        self.root = WordNode(None, None)

    def add_sentence(self, sentence: str, source_file: str) -> None:
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

    def search_sentence_prefix(self, wordTrie, prefix):
        words = prefix.split()
        if not words:
            return []

        # Recherche du premier mot dans le Word Trie
        first_word_refs = wordTrie.search_prefix(words[0])
        if not first_word_refs:
            return []

        # Filtrage des références du premier mot dans le Sentence Trie
        valid_refs = []
        for word, frequency, refs in first_word_refs:
            for ref in refs:

                node = ref
                valid = True
                for word in words[1:]:
                    found = False
                    for child in node.children:
                        if child.word == word:
                            node = child
                            found = True
                            break
                    if not found:
                        valid = False
                        break
                if valid:
                    valid_refs.append(node)

        # Reconstruction et complétion de la phrase
        complete_sentences_with_sources = []
        for node in valid_refs:
            sentences, source = self.reconstruct_sentence(node)
            for sentence in sentences:
                complete_sentences_with_sources.append((sentence, source))

        return complete_sentences_with_sources

    def get_best_k_completions(self, prefix: str, wordTrie, k: int) -> typing.List[word_trie.AutoCompleteData]:
        results = []

        # Search for exact matches
        exact_matches = self.search_sentence_prefix(wordTrie, prefix)
        for sentence, source in exact_matches:
            score = 2 * len(prefix)
            results.append(AutoCompleteData(sentence, source, 0, score))

        # If exact matches are less than k, find possible corrections
        if len(results) < k:
            possible_corrections = []

            # Substitute a letter
            possible_corrections.extend(substitute_letter(self, prefix, wordTrie))

            # Add a missing letter
            possible_corrections.extend(add_missing_letter(self, prefix, wordTrie))

            # Remove an extra letter
            possible_corrections.extend(remove_extra_letter(self, prefix, wordTrie))

            all_results = sorted(results + possible_corrections, key=lambda x: x.score, reverse=True)
            return all_results[:k]

        return sorted(results, key=lambda x: x.score, reverse=True)[:k]

def substitute_letter(sentence_trie, prefix, word_trie):
    possible_corrections = []
    for i in range(len(prefix)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != prefix[i]:
                corrected_prefix = prefix[:i] + char + prefix[i + 1:]
                corrected_matches = sentence_trie.search_sentence_prefix(word_trie, corrected_prefix)
                for sentence, source in corrected_matches:
                    score = calculate_substitution_score(prefix, corrected_prefix)
                    possible_corrections.append(AutoCompleteData(sentence, source, 0, score))
    return possible_corrections
def remove_extra_letter(sentence_trie, prefix, word_trie):
    possible_corrections = []
    for i in range(len(prefix)):
        corrected_prefix = prefix[:i] + prefix[i + 1:]
        corrected_matches = sentence_trie.search_sentence_prefix(word_trie, corrected_prefix)
        for sentence, source in corrected_matches:
            score = calculate_add_remove_score(prefix, corrected_prefix)
            possible_corrections.append(AutoCompleteData(sentence, source, 0, score))
    return possible_corrections


def add_missing_letter(sentence_trie, prefix: str, word_trie) -> typing.List[AutoCompleteData]:
    possible_corrections = []
    for i in range(len(prefix) + 1):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            corrected_prefix = prefix[:i] + char + prefix[i:]
            corrected_matches = sentence_trie.search_sentence_prefix(word_trie, corrected_prefix)
            for sentence, source in corrected_matches:
                score = calculate_add_remove_score(prefix, corrected_prefix)
                possible_corrections.append(AutoCompleteData(sentence, source, 0, score))
    return possible_corrections

def calculate_substitution_score(prefix: str, corrected_prefix: str) -> int:
    base_score = 2 * len(prefix)
    penalties = 0
    for i, (p_char, c_char) in enumerate(zip(prefix, corrected_prefix)):
        if p_char != c_char:
            if i == 0:
                penalties += 5
            elif i == 1:
                penalties += 4
            elif i == 2:
                penalties += 3
            elif i == 3:
                penalties += 2
            else:
                penalties += 1
    return base_score - penalties

def calculate_add_remove_score(prefix: str, corrected_prefix: str) -> int:
    base_score = 2 * len(prefix)
    penalties = 0
    length_diff = abs(len(prefix) - len(corrected_prefix))
    if length_diff > 0:
        for i in range(length_diff):
            if i == 0:
                penalties += 10
            elif i == 1:
                penalties += 8
            elif i == 2:
                penalties += 6
            elif i == 3:
                penalties += 4
            else:
                penalties += 2
    return base_score - penalties
