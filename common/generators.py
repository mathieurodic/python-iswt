import random


def capital_identifier(length):
    return ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        for i in range(length)
    )

def wordlike_identifier(length):
    is_vowel = bool(random.getrandbits(1))
    identifier = ''
    for i in range(length):
        identifier += random.choice(
            'AEIOU'
            if is_vowel else
            'ZRTYPMLKJHFDWVBN'
        )
        is_vowel = not is_vowel
    return identifier

def sentence(words_count, min_word_length, max_word_length):
    return ' '.join(
        wordlike_identifier(random.randrange(min_word_length, max_word_length + 1))
        for w in range(words_count)
    ).capitalize() + '.'
