# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 18:22:50 2026

@author: Amir
"""

def caesar_cipher(text, shift):
    result = ""

    for ch in text:
        if ch == " ":
            result += ch
        elif 'A' <= ch <= 'Z':
            original_index = ord(ch) - ord('A')
            new_index = (original_index + shift) % 26
            new_char = chr(ord('A') + new_index)
            result += new_char
        elif 'a' <= ch <= 'z':
            original_index = ord(ch) - ord('a')
            new_index = (original_index + shift) % 26
            new_char = chr(ord('a') + new_index)
            result += new_char
        else:
            result += ch

    return result


def caesar_decipher(ciphertext, shift):
    result = ""

    for ch in ciphertext:
        if ch == " ":
            result += ch
        elif 'A' <= ch <= 'Z':
            original_index = ord(ch) - ord('A')
            new_index = (original_index - shift) % 26
            new_char = chr(ord('A') + new_index)
            result += new_char
        elif 'a' <= ch <= 'z':
            original_index = ord(ch) - ord('a')
            new_index = (original_index - shift) % 26
            new_char = chr(ord('a') + new_index)
            result += new_char
        else:
            result += ch

    return result


def letter_frequency(text):
    freq = {}

    for ch in text:
        ch = ch.lower()
        if 'a' <= ch <= 'z':
            if ch in freq:
                freq[ch] += 1
            else:
                freq[ch] = 1

    return freq


def main():
    while True:
        print("\n=== Caesar Cipher Menu ===")
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Show letter frequency")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            text = input("Enter text to encrypt: ")
            shift = int(input("Enter shift value: "))
            encrypted = caesar_cipher(text, shift)
            print("Encrypted text:", encrypted)

        elif choice == "2":
            text = input("Enter text to decrypt: ")
            shift = int(input("Enter shift value: "))
            decrypted = caesar_decipher(text, shift)
            print("Decrypted text:", decrypted)

        elif choice == "3":
            text = input("Enter text: ")
            freq = letter_frequency(text)
            print("Letter frequency:")
            for letter in sorted(freq.keys()):
                print(letter, ":", freq[letter])

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1–4.")


if __name__ == "__main__":
    main()
    