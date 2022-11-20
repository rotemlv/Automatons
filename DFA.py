import copy
import random
from collections.abc import Hashable, Callable
# import tqdm


class DeterministicFiniteAutomaton:
    # automata represented as a "graph" over a language
    language: set
    states: set
    initial_state: Hashable
    delta: dict
    accepting_states: set

    def __init__(self, language=None):
        self.language = language if language is not None else set()
        self.states = set()
        self.delta = {}
        self.accepting_states = set()

        # initial state's delta must be manually defined
        self.initial_state = 0
        self.states.add(self.initial_state)

    def set_language(self, language: set):
        self.language = language

    def add_state(self, state: Hashable):
        self.states.add(state)

    def set_accepting_state(self, state: Hashable):
        assert state in self.states
        self.accepting_states.add(state)

    def add_state_with_delta(self, state: Hashable, delta_for_state: dict):
        # check format of delta
        assert (len(key) == 2 and key[0] in self.states for key in delta_for_state.keys())
        # delta must be of the form dict[state, letter] = any_state FOR EACH LETTER in alphabet
        # as in: delta must cover the language (DFA)
        tmp = set([d[1] for d in delta_for_state.keys()])
        for letter in self.language:
            assert letter in tmp
            # specific delta is not already defined in language
            # TODO: add option to replace delta of a given input
            assert self.delta.get((state, letter)) is None

        self.states.add(state)
        self.delta = {**self.delta, **delta_for_state}

    def add_delta(self, delta: dict):
        for elem in delta.keys():

            # check we didn't add a traversal from the same state and letter before
            assert self.delta.get(elem) is None
            # check that all states are there
            assert elem[0] in self.states
            # check that letter is there
            assert elem[1] in self.language
        # add delta
        self.delta = {**self.delta, **delta}

    def traverse(self, word: str):
        assert all(letter in self.language for letter in word)
        state = self.initial_state
        consumable_word = copy.copy(word)
        while len(consumable_word):
            print(f"state before reading: {state}", end='; ')
            t = consumable_word[0]
            consumable_word = consumable_word[1:]
            print(f"reading letter: {t}", end='; ')
            state = self.delta[(state, t)]
            print(f"moved to state {state}")
        print(f"Finished reading {word}, final state: {state}")

    def traverse_silent_return_state(self, word: str):
        """Automata traverses the word and returns the word's final state"""
        assert all(letter in self.language for letter in word)
        state = self.initial_state
        consumable_word = copy.copy(word)
        while len(consumable_word):
            t = consumable_word[0]
            consumable_word = consumable_word[1:]
            state = self.delta[(state, t)]
        return state

    def check_if_word_in_automata_s_language(self, word: str):
        """Returns True iff automata accepts the word"""
        return self.traverse_silent_return_state(word) in self.accepting_states


def random_word(language: set, length: int):
    letters = list(language)
    letters_count = len(letters)
    last_idx = letters_count - 1
    return "".join((letters[random.randint(0, last_idx)] for _ in range(length)))


def independent_language_check(regular_expression: Callable, word: str):
    """Code a test for a word's presence in a language.
        Call this to test the returns of an automata which rolls over millions of words."""
    return regular_expression(word)


def check_if_word_is_a_odd_b_odd_str(word: str):
    """Example test function
        :returns True iff word accepted by DFA"""
    tmp = word.find('b')
    supposed_a_segment = word[:tmp]
    supposed_b_segment = word[tmp:]
    # can't have 'a' after 'b'
    if 'a' in supposed_b_segment:
        return False
    # 'a' count and 'b' count must be odd
    if (len(supposed_a_segment) % 2 == 0) or (len(supposed_b_segment) % 2 == 0):
        return False
    return True
