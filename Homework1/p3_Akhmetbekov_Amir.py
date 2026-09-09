# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:46:10 2026

@author: Amir
"""

def find_dup_str(s, n):
    if n >= 4:
        return "xxx"

    for i in range(len(s) - n + 1):
        substring = s[i:i+n]

        for j in range(i + n, len(s) - n + 1):
            if s[j:j+n] == substring:
                return substring

    return ""


def find_max_dup(s):
    longest = ""

    for n in range(1, len(s) + 1):
        result = find_dup_str(s, n)

        if result == "xxx":
            break

        if result != "":
            longest = result

    return longest


# Test part a
s = input("Enter a string: ")
n = int(input("Enter substring length: "))

print(find_dup_str(s, n))


# Test part b
s = input("Enter a string for longest duplicated substring: ")

print(find_max_dup(s))
