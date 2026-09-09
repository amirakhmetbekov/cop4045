# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 11:04:06 2026

@author: Amir
"""

import math
import matplotlib.pyplot as plt

while True:
    a_input = input("Enter coefficient a (press ENTER to quit): ")

    if a_input == "":
        break

    a = float(a_input)
    b = float(input("Enter coefficient b: "))
    c = float(input("Enter coefficient c: "))

    discriminant = b**2 - 4*a*c

    # Determine the solutions and x-domain
    if discriminant < 0:
        print("no real solutions")

        # Center the domain on the vertex
        x_center = -b / (2*a)
        x_min = x_center - 5
        x_max = x_center + 5

    elif discriminant == 0:
        x1 = -b / (2*a)

        print("one solution:", x1)

        # Make sure the root is visible
        x_min = x1 - 1
        x_max = x1 + 1

    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)

        print("two solutions:", x1, x2)

        # Make sure both roots are visible
        x_min = min(x1, x2) - 1
        x_max = max(x1, x2) + 1

    # Generate exactly 150 x-values
    x_values = []

    for i in range(150):
        x = x_min + i * (x_max - x_min) / 149
        x_values.append(x)

    # Calculate corresponding y-values
    y_values = []

    for x in x_values:
        y = a * x**2 + b * x + c
        y_values.append(y)

    # Plot the quadratic function
    plt.plot(x_values, y_values)

    plt.axhline(0)
    plt.axvline(0)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Quadratic Function")
    plt.grid()

    plt.show()
    