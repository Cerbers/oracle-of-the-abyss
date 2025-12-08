from oracle.syllable_counter import DICTIONARY_CMUDICT


# note: this function is meant to pull words that have only one syllable variant
# the word object must be called for words that do not have single syllable variants
# comment to be deleted after implementing word object usage throughout the codebase
def pull_single_syllable_variant_from_words(words: list[str]) -> list[str]:
    """
    After receiving a list of words, return only those words that have a single syllable variant.
    If a word has more than 1 syllable pronunciation variant and the variants have different syllable counts,
    it is excluded from the returned list.
    """
    
    single_syllable_variants = []
    for word in words:
        if word in DICTIONARY_CMUDICT:
            syllable_counts = set(len([ph for ph in pronunciation if ph[-1].isdigit()]) for pronunciation in DICTIONARY_CMUDICT[word])
            if len(syllable_counts) == 1:
                single_syllable_variants.append(word)
    return single_syllable_variants


# BASE ALGORITHM FOR SIMPLE SYLLABLE PATTERN DETECTION

