#!/usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

from matplotlib.backend_bases import MouseButton


def add_point(x, y):
    offsets = scatter.get_offsets()
    points = np.array([[x, y]])

    offsets = np.concatenate([offsets, points])

    scatter.set_offsets(offsets)
    fig.canvas.draw()

    save()


def undo():
    offsets = scatter.get_offsets()

    offsets = offsets[:-1]

    scatter.set_offsets(offsets)
    fig.canvas.draw()

    save()


def save():
    offsets = scatter.get_offsets()

    df = pd.DataFrame(offsets, columns=["x", "y"])
    df.to_csv(args.output, index=False, sep="\t")


def onclick(event):
    if event.button == MouseButton.LEFT:
        add_point(event.xdata, event.ydata)
    elif event.button == MouseButton.RIGHT:
        undo()


def main(argv=None):
    global fig
    global ax
    global args
    global scatter

    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--xmin", default=0, type=float)
    parser.add_argument("--xmax", default=1, type=float)
    parser.add_argument("--ymin", default=0, type=float)
    parser.add_argument("--ymax", default=1, type=float)
    parser.add_argument("-o", "--output", default="out.csv")

    args = parser.parse_args(argv)

    img = mpimg.imread(args.image)

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[args.xmin, args.xmax, args.ymin, args.ymax], aspect="auto")
    scatter = ax.scatter([], [])
    fig.canvas.mpl_connect("button_press_event", onclick)
    plt.show()


if __name__ == "__main__":
    main()
