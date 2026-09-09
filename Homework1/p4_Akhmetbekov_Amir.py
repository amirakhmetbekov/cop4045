# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:00:16 2026

@author: Amir
"""

import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    xmin = domain[0]
    xmax = domain[1]

    xs = []
    ys = []

    step = (xmax - xmin) / (ns - 1)

    for i in range(ns):
        x = xmin + i * step
        xs.append(x)

    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("      x          y")
    print("---------------------")

    for i in range(ns):
        print("{:8.4f} {:+10.4f}".format(xs[i], ys[i]))

    plt.plot(xs, ys, "o-")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.grid()
    plt.show()


fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))

domain = (xmin, xmax)

plot_function(fun_str, domain, ns)