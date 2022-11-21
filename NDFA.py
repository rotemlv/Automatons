import copy
from random import randint
from DFA import DFA, random_word


class NDFA(DFA):
    def __init__(self, language: set = None):
        super().__init__(language)

    def traverse(self, input_word: str):
        """Verbose read of a word by the calling NDFA"""
        assert all(letter in self.language for letter in input_word)
        state = self.initial_state
        consumable_word = copy.copy(input_word)
        is_stuck = False
        while len(consumable_word):
            print(f"state before reading: {state}", end='; ')
            t = consumable_word[0]
            consumable_word = consumable_word[1:]
            print(f"reading letter: {t}", end='; ')
            possible_states = self.delta.get((state, t))
            if possible_states is None:
                is_stuck = True
                break
            if isinstance(possible_states, list):
                rnd_state = possible_states[randint(0, len(possible_states) - 1)]
            else:
                raise Exception("Delta should be a map of the form"
                                " (state, letter) -> <list of states>")
            # grab a random state from the dict
            state = rnd_state

            print(f"moved to state {state}")
        print(f"Finished reading {input_word}, final state: {state}")
        if is_stuck:
            print(f"Automata got stuck at {state}, word NOT accepted")

    def traverse_with_boolean_answer(self, word: str):
        """Returns True if the given word has been accepted by the NDFA.
        Important: False does not mean the word has been rejected,
        rather that the run has not accepted the word."""
        assert all(letter in self.language for letter in word)
        state = self.initial_state
        consumable_word = copy.copy(word)
        is_stuck = False
        while len(consumable_word):
            t = consumable_word[0]
            consumable_word = consumable_word[1:]
            possible_states = self.delta.get((state, t))
            if possible_states is None:
                is_stuck = True
                break
            if isinstance(possible_states, list):
                rnd_state = possible_states[randint(0, len(possible_states) - 1)]
            else:
                raise Exception("Delta should be a map of the form"
                                " (state, letter) -> <list of states>")
            # grab a random state from the dict
            state = rnd_state
        if is_stuck:
            return False
        return state in self.accepting_states

    def total_traverse_with_boolean_answer(self, word: str, initial_state=None):
        """Returns True iff the given word has been accepted by the NDFA.
        In practice: traverses ALL possible paths over the NDFA."""
        assert all(letter in self.language for letter in word)
        if initial_state is None:
            initial_state = self.initial_state
        state = initial_state
        consumable_word = copy.copy(word)
        is_stuck = False

        while len(consumable_word):
            t = consumable_word[0]
            consumable_word = consumable_word[1:]
            possible_states = self.delta.get((state, t))
            if possible_states is None:
                is_stuck = True
                break
            if isinstance(possible_states, list):
                # traverse ALL paths from current state given some letter

                return any(self.total_traverse_with_boolean_answer(consumable_word, s)
                           for s in possible_states)
            else:
                raise Exception("Delta should be a map of the form"
                                " (state, letter) -> <list of states>")
            # grab a random state from the dict
        if is_stuck:
            return False
        return state in self.accepting_states
