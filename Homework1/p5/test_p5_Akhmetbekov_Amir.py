# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:02:53 2026

@author: Amir
"""

import unittest
from p5_Akhmetbekov_Amir import caesar_cipher, caesar_decipher, letter_frequency

class TestCaesarCipher(unittest.TestCase):

    def test_caesar_cipher_basic(self):
        self.assertEqual(caesar_cipher("abc", 1), "bcd")
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_caesar_cipher_mixed_case(self):
        self.assertEqual(caesar_cipher("AbC", 2), "CdE")

    def test_caesar_cipher_spaces(self):
        self.assertEqual(caesar_cipher("a b c", 1), "b c d")

    def test_caesar_decipher_basic(self):
        self.assertEqual(caesar_decipher("bcd", 1), "abc")
        self.assertEqual(caesar_decipher("abc", 3), "xyz")

    def test_caesar_decipher_mixed_case(self):
        self.assertEqual(caesar_decipher("CdE", 2), "AbC")

    def test_letter_frequency_basic(self):
        freq = letter_frequency("aabbc")
        self.assertEqual(freq, {"a": 2, "b": 2, "c": 1})

    def test_letter_frequency_ignore_case(self):
        freq = letter_frequency("AaBbC")
        self.assertEqual(freq, {"a": 2, "b": 2, "c": 1})

    def test_letter_frequency_ignore_non_letters(self):
        freq = letter_frequency("a!b?c 123")
        self.assertEqual(freq, {"a": 1, "b": 1, "c": 1})


if __name__ == "__main__":
    unittest.main()
