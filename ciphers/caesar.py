"""
Caesar Cipher Implementation

This module implements encryption, decryption, and basic cryptanalysis
for the classical Caesar cipher. Intended for educational use only.
"""

import string
from typing import Tuple, List

ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = len(ALPHABET)


# -----------------------------
# Core Caesar Cipher Functions
# -----------------------------

def encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt plaintext using a Caesar cipher.

    Args:
        plaintext (str): Input text (expected uppercase A–Z and spaces)
        shift (int): Shift value (0–25)

    Returns:
        str: Encrypted ciphertext
    """
    shift = shift % ALPHABET_SIZE
    ciphertext = []

    for char in plaintext:
        if char in ALPHABET:
            idx = (ALPHABET.index(char) + shift) % ALPHABET_SIZE
            ciphertext.append(ALPHABET[idx])
        else:
            ciphertext.append(char)

    return ''.join(ciphertext)


def decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypt Caesar-encrypted ciphertext.

    Args:
        ciphertext (str): Encrypted text
        shift (int): Shift value used during encryption

    Returns:
        str: Decrypted plaintext
    """
    return encrypt(ciphertext, -shift)


# -----------------------------
# Attacks on Caesar Cipher
# -----------------------------

def brute_force_attack(ciphertext: str) -> List[Tuple[int, str]]:
    """
    Try all possible Caesar shifts.

    Args:
        ciphertext (str): Encrypted text

    Returns:
        List of (shift, decrypted_text)
    """
    results = []

    for shift in range(ALPHABET_SIZE):
        decrypted = decrypt(ciphertext, shift)
        results.append((shift, decrypted))

    return results


def frequency_attack(ciphertext: str, score_func) -> Tuple[int, str]:
    """
    Perform frequency-analysis-based attack.

    Args:
        ciphertext (str): Encrypted text
        score_func (callable): Function that scores English-likeness

    Returns:
        (best_shift, best_guess)
    """
    best_score = float('-inf')
    best_shift = None
    best_plaintext = None

    for shift in range(ALPHABET_SIZE):
        candidate = decrypt(ciphertext, shift)
        score = score_func(candidate)

        if score > best_score:
            best_score = score
            best_shift = shift
            best_plaintext = candidate

    return best_shift, best_plaintext


# -----------------------------
# Utility / Validation
# -----------------------------

def validate_shift(shift: int):
    if not isinstance(shift, int):
        raise TypeError("Shift must be an integer.")
    if shift < 0 or shift >= ALPHABET_SIZE:
        raise ValueError("Shift must be in range 0–25.")
