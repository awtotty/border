from audioop import cross
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from perlin_noise import PerlinNoise

from border import crossings_in_year


# https://en.wikipedia.org/wiki/Perlin_noise
# https://predictablynoisy.com/matplotlib/gallery/images_contours_and_fields/custom_cmap.html#sphx-glr-gallery-images-contours-and-fields-custom-cmap-py


BLUE = (0, 0, 1, 1)
RED = (1, 0, 0, 1)
WHITE = (1, 1, 1, 1)
MAROON = (0.7, 0, 0, 1)
GREEN = (0, 0.8, 0, 1)
TRANSPARENT = (0, 0, 0, 0)


years = range(2018, 2022)
crossings = [crossings_in_year(yr) for yr in years]

# octaves = [0.5, 1.5, 0.5, 1.5]
octaves = [1+c/sum(crossings) for c in crossings]

seeds = years

fig, axs = plt.subplots(2, 2, figsize=(6, 9))
# fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94, wspace=0.05)
for o, yr, seed, ax in zip(octaves, years, seeds, axs.ravel()):
    # can replace Perlin noise with other noise function (based on data?)
    noise = PerlinNoise(octaves=o, seed=seed)
    xpix, ypix = 40, 40
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

    colors = [
        BLUE, 
        RED, 
        TRANSPARENT, 
        TRANSPARENT, 
        WHITE, 
        TRANSPARENT, 
        TRANSPARENT, 
        MAROON, 
        GREEN,
    ]

    # Fewer bins will result in "coarser" colormap interpolation
    n_bin = len(colors)
    cm = LinearSegmentedColormap.from_list("my_list", colors, N=n_bin)

    # note: origin='lower' flips image horizontally
    # im = ax.imshow(pic, interpolation='nearest', origin='lower', cmap=cm)
    im = ax.imshow(pic, cmap=cm)
    ax.set_title(f"Octaves: {round(o, 2)}, Yr: {yr}")

    # plot clean up
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

plt.savefig("regions.png", transparent=True)

