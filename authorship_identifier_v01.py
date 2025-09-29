#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Authorship Identification Program - Version 1
Based on Chapter 11 of Learn AI-Assisted Python Programming
"""

import string


# =============================================================================
# LOW-LEVEL HELPER FUNCTIONS
# =============================================================================

def clean_word(word):
    """
    Return lowercase version of word with punctuation stripped from ends.
    >>> clean_word('Pearl!')
    'pearl'
    """
    word = word.lower()
    word = word.strip()
    word = word.strip(string.punctuation)
    return word


def split_string(text, separators):
    """
    Split text using any character in separators.
    >>> split_string('one*two [three', '*[')
    ['one', 'two', 'three']
    """
    words = []
    word = ''
    for char in text:
        if char in separators:
            word = word.strip()
            if word != '':
                words.append(word)
            word = ''
        else:
            word += char
    word = word.strip()
    if word != '':
        words.append(word)
    return words


def get_sentences(text):
    """Return list of sentences from text."""
    return split_string(text, '.?!')


def get_phrases(sentence):
    """Return list of phrases from sentence."""
    return split_string(sentence, ',;:')


# =============================================================================
# FEATURE CALCULATION FUNCTIONS
# =============================================================================

def average_word_length(text):
    """Return average word length in text."""
    words = text.split()
    total = 0
    count = 0
    for word in words:
        word = clean_word(word)
        if word != '':
            total += len(word)
            count += 1
    return total / count if count > 0 else 0


def different_to_total(text):
    """Return ratio of unique words to total words."""
    words = text.split()
    total = 0
    unique = set()
    for word in words:
        word = clean_word(word)
        if word != '':
            total += 1
            unique.add(word)
    return len(unique) / total if total > 0 else 0


def exactly_once_to_total(text):
    """Return ratio of words appearing exactly once to total words."""
    words = text.split()
    total = 0
    unique = set()
    once = set()
    for word in words:
        word = clean_word(word)
        if word != '':
            total += 1
            if word in unique:
                once.discard(word)
            else:
                unique.add(word)
                once.add(word)
    return len(once) / total if total > 0 else 0


def average_sentence_length(text):
    """Return average number of words per sentence."""
    sentences = get_sentences(text)
    if not sentences:
        return 0
    word_counts = [len(sentence.split()) for sentence in sentences]
    total_words = sum(word_counts)
    return total_words / len(sentences)


def average_sentence_complexity(text):
    """Return average number of phrases per sentence."""
    sentences = get_sentences(text)
    if not sentences:
        return 0
    total = 0
    for sentence in sentences:
        phrases = get_phrases(sentence)
        total += len(phrases)
    return total / len(sentences)


# =============================================================================
# SIGNATURE FUNCTIONS
# =============================================================================

def make_signature(text):
    """
    Return signature for text: [avg_word_len, unique_ratio,
    once_ratio, avg_sent_len, avg_complexity]
    """
    return [
        average_word_length(text),
        different_to_total(text),
        exactly_once_to_total(text),
        average_sentence_length(text),
        average_sentence_complexity(text)
    ]


def get_all_signatures(texts_dict):
    """
    texts_dict maps author names to text strings.
    Return dict mapping author names to signatures.
    """
    signatures = {}
    for author, text in texts_dict.items():
        signatures[author] = make_signature(text)
    return signatures


# =============================================================================
# PREDICTION FUNCTIONS
# =============================================================================

def get_score(sig1, sig2, weights):
    """Calculate weighted difference between two signatures."""
    score = 0
    for i in range(len(sig1)):
        score += abs(sig1[i] - sig2[i]) * weights[i]
    return score


def make_guess(signatures_dict, mystery_signature, weights):
    """Return author name with signature closest to mystery_signature."""
    lowest_author = None
    lowest_score = None

    for author, signature in signatures_dict.items():
        score = get_score(signature, mystery_signature, weights)
        if lowest_score is None or score < lowest_score:
            lowest_score = score
            lowest_author = author

    return lowest_author


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Sample texts from Chapter 11
    texts = {
        'Agatha Christie': """
        The Murder at the Vicarage is a work of detective fiction. 
        It features Miss Marple, one of Christie's most beloved characters. 
        The story unfolds in the quaint village of St. Mary Mead.
        """,

        'Arthur Conan Doyle': """
        The Hound of the Baskervilles is perhaps the most famous tale. 
        Sherlock Holmes investigates a supernatural legend. 
        Watson accompanies him to the eerie moors of Devonshire.
        """,

        'Jane Austen': """
        Pride and Prejudice remains a beloved classic of English literature.
        Elizabeth Bennet is a spirited and intelligent protagonist.
        The novel explores themes of love, class, and social expectations.
        """
    }

    # Create signatures
    print("=== Creating Author Signatures ===")
    signatures = get_all_signatures(texts)
    for author, sig in signatures.items():
        print(f"{author}: {sig}")

    # Test with mystery text
    mystery = """
        The mysterious death occurred on a foggy evening.
        Holmes examined the evidence with his characteristic precision.
        Watson took careful notes of every detail.
    """

    print("\n=== Making Prediction ===")
    mystery_sig = make_signature(mystery)
    print(f"Mystery signature: {mystery_sig}")

    weights = [11, 33, 50, 0.4, 4]
    guess = make_guess(signatures, mystery_sig, weights)
    print(f"\nPredicted author: {guess}")