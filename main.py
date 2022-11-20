from random import randint
from DFA import random_word
from NDFA import NonDeterministicAutomaton

if __name__ == '__main__':
    NA = NonDeterministicAutomaton({'a', 'b'})
    NA.add_state(0)
    NA.add_state(1)
    NA.set_accepting_state(0)
    NA.add_delta({(1, 'a'): [0, 1], (1, 'b'): [0], (0, 'a'): [1]})
    # NA.traverse("abbaaa")

    random_words = set()
    while len(random_words) < 10:
        random_words.add(random_word({'a', 'b'}, randint(0, 20)))

    accepted_words = set()
    for w in random_words:
        if NA.total_traverse_with_boolean_answer(w):
            accepted_words.add(w)

    print("Words accepted by avtamat:")
    print(accepted_words)
    print("Words rejected by avtamat:")
    print(random_words - accepted_words)
