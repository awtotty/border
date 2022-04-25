import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from perlin_noise import PerlinNoise

from border import crossings_in_year
from my_noise import MyNoise


# https://en.wikipedia.org/wiki/Perlin_noise
# https://predictablynoisy.com/matplotlib/gallery/images_contours_and_fields/custom_cmap.html#sphx-glr-gallery-images-contours-and-fields-custom-cmap-py


# TODO: 
# https://en.wikipedia.org/wiki/Procedural_texture
# https://en.wikipedia.org/wiki/Procedural_texture#Self-organizing_textures 
# https://www.labri.fr/perso/nrougier/from-python-to-numpy/#exercise 


# BLUE = (0.1, 0.1, 0.1, 1)
# RED = (0.3, 0.3, 0.3, 1)
# WHITE = (1, 1, 1, 1)
# MAROON = (0.7, 0.7, 0.7, 1)
# GREEN = (0, 0, 0, 1)
# TRANSPARENT = (0, 0, 0, 0)

BLUE = (0, 0, 1, 0.5)
RED = (0.7, 0.1, 0.26, 0.9)
WHITE = (1, 1, 1, 0.85)
MAROON = (0.78, 0.06, 0.18, 0.9)
GREEN = (0, 0.39, 0.25, 0.7)
TRANSPARENT = (0, 0, 0, 0)

US_POP = 332_900_000
MEXICO_POP = 129_200_000


def generate_image(octaves, size, seed, ax, no_frame=False): 
    xpix, ypix = size
    # can replace Perlin noise with other noise function (based on data?)
    noise = PerlinNoise(octaves=octaves, seed=seed)
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

    colors = [
        BLUE, 
        TRANSPARENT, 
        RED, 
        TRANSPARENT, 
        TRANSPARENT, 
        WHITE, 
        TRANSPARENT, 
        TRANSPARENT, 
        MAROON, 
        TRANSPARENT, 
        GREEN,
    ]

    # Fewer bins will result in "coarser" colormap interpolation
    n_bin = len(colors)
    cm = LinearSegmentedColormap.from_list("my_list", colors, N=n_bin)

    # note: origin='lower' flips image horizontally
    # im = ax.imshow(pic, interpolation='nearest', origin='lower', cmap=cm)
    im = ax.imshow(pic, cmap=cm)

    # plot clean up
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    if no_frame: 
        ax.axis('off')

    return ax


def generate_demo(): 
    years = range(2018, 2022)
    crossings = [crossings_in_year(yr) for yr in years]
    # octaves = [1+c/sum(crossings) for c in crossings]
    # octaves = [c/sum(crossings) for c in crossings]
    # octaves = [1 + 1/(1 + c/(US_POP+MEXICO_POP)) for c in crossings]
    octaves = range(1,5)
    seeds = years

    fig, axs = plt.subplots(2, 2, figsize=(6, 9))
    # fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94, wspace=0.05)
    for o, yr, seed, ax in zip(octaves, years, seeds, axs.ravel()):
        xpix, ypix = 12, 12
        ax  = generate_image(o, (xpix, ypix), seed, ax)
        ax.set_title(f"Octaves: {round(o, 2)}, Yr: {yr}")

    plt.savefig("regions.png", transparent=True)


def generate_samples_seeds(seeds=None, size=(15, 10)):
    if seeds is None: 
        seeds = range(1, 25)

    year = 2021
    crossings = crossings_in_year(year)
    # octaves = 1 + crossings/(US_POP+MEXICO_POP)    
    # octaves = 2 * crossings/(US_POP+MEXICO_POP)    
    # octaves = 1 + 5 * crossings/(US_POP+MEXICO_POP)    
    octaves = get_octaves(crossings)
    print(f"octaves: {octaves}")
    xpix, ypix = size
    
    for i, seed in enumerate(seeds): 
        fig, ax = plt.subplots(1, 1, figsize=(1, 1))
        ax = generate_image(octaves, (xpix, ypix), seed, ax, no_frame=True)
        ax.set_title(f"Seed: {seed}")
        plt.savefig(f"img/seed_samples/seed_sample_{seed}.png", transparent=True, dpi=500)
        plt.close(fig)

def get_octaves(crossings): 
    return 1 + 5 * crossings/(US_POP+MEXICO_POP)    


def generate_final(seed, size=(15, 10)): 
    year = 2021
    crossings = crossings_in_year(year)
    # octaves = 1 + 5 * crossings/(US_POP+MEXICO_POP)    
    octaves = get_octaves(crossings)
    fig, ax = plt.subplots(1, 1, figsize=(1,1))
    generate_image(octaves, size, seed, ax, no_frame=True)

    plt.savefig("final.png", transparent=True, dpi=1000)


def main():
    # generate_demo()

    # seeds = range(1, 51) 
    seeds = range(1, 101) 
    # size=(15,10) works for original image
    # generate_samples_seeds(seeds) 

    # size=(14,10) for crop (but it's not perfect)
    # generate_samples_seeds(seeds, size=(14,10)) 

    # square 
    generate_samples_seeds(seeds, size=(10,10)) 

    # generate_final(seed=46)


if __name__ == '__main__': 
    main()