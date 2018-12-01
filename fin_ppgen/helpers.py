"""Helper functions for the passphrase generator"""

import re
import secrets

# This approach of handling the necessary regex functions by using closures
# to dynamically build the functions is taken from Dive into Python 3
# by Mark Pilgrim (see http://www.diveintopython3.net/generators.html)
def build_inflect_functions(pattern, search, replace):
    """Dynamically build regex search and replace functions."""

    def match_rule(word):
        return re.search(pattern, word)

    def inflect_rule(word):
        return re.sub(search, replace, word)

    return (match_rule, inflect_rule)


def initialize_rules(pattern_file):
    """A helper function for extracting regex search and replace rules
       from an external file."""

    rules = []
    with open(pattern_file, encoding='utf-8') as fp:
        for line in fp:
            if line[0] in ['#', '\n', '\r']:  # skip comments and empty lines
                continue
            pattern, search, replace = line.split(None, 3)
            rules.append(build_inflect_functions(pattern, search, replace))

    return rules


def random_set(word_list, size_of_set):
    """Randomly select a subset of the input word list."""
    random_entries = [secrets.choice(word_list) for i in range(size_of_set)]
    return random_entries
