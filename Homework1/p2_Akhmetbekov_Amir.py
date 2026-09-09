# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 12:51:51 2026

@author: Amir
"""

def find_Pythagorean(n):
    triples = []

    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            for c in range(b + 1, n + 1):
                if a**2 + b**2 == c**2:
                    triples.append((a, b, c))

    return triples


n = int(input("Enter a positive integer n: "))

triples = find_Pythagorean(n)

for triple in triples:
    print(triple)
    