"""
Frequency analysis utilities for classical cryptanalysis.

Provides letter frequency calculation and English-likeness
scoring using the chi-squared statistic.
"""

import string
from typing import Dict

ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = len(ALPHABET)


# --------------------------------
# Reference English Frequencies
# Based on statistics from Emory University:
# https://mathcenter.oxford.emory.edu/site/math125/englishLetterFreqs/
# --------------------------------

ENGLISH_LETTER_FREQ: Dict[str, float] = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
    'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
    'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
    'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
    'Y': 0.01974, 'Z': 0.00074
}


# --------------------------------
# Frequency Computation
# --------------------------------

def letter_frequency(text: str) -> Dict[str, float]:
    """
    Compute normalized letter frequency of A–Z in text.

    Args:
        text (str): Input text (uppercase recommended)

    Returns:
        Dict[str, float]: Frequency distribution
    """
    counts = {char: 0 for char in ALPHABET}
    total_letters = 0

    for char in text:
        if char in ALPHABET:
            counts[char] += 1
            total_letters += 1

    if total_letters == 0:
        return counts

    return {char: counts[char] / total_letters for char in ALPHABET}


# --------------------------------
# Scoring Functions
# --------------------------------

def chi_squared_score(text: str) -> float:
    """
    Compute chi-squared statistic against English letter frequencies.

    Lower score = more English-like.

    Args:
        text (str): Candidate plaintext

    Returns:
        float: Chi-squared score
    """
    observed = letter_frequency(text)
    total = sum(1 for c in text if c in ALPHABET)

    if total == 0:
        return float('inf')

    chi2 = 0.0
    for char in ALPHABET:
        expected = ENGLISH_LETTER_FREQ[char] * total
        actual = observed[char] * total

        if expected > 0:
            chi2 += (actual - expected) ** 2 / expected

    return chi2


def english_score(text: str) -> float:
    """
    Convert chi-squared score into a maximization score.

    Higher = better match to English.
    """
    return -chi_squared_score(text)
