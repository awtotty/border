from typing import Iterable
import numpy as np

from border import crossings_in_year


# https://www.cbp.gov/newsroom/stats/southwest-land-border-encounters
encounters_dict = {
    2019: 977_509, 
    2020: 458_088,
    2021: 1_734_686,
}

class MyNoise: 
    def __init__(self, year, size=(10,10), seed=1) -> None:
        self.crossings = crossings_in_year(year) 
        self.encounters = encounters_dict[year]
        self.p = self.encounters / (self.crossings+self.encounters)
        np.random.seed(seed)
        self.vals = np.random.random_sample(size)
        self.vals[self.vals < self.p] = 0

    def noise(self, pos: Iterable) -> float: 
        idx = np.multiply(self.vals.shape, pos).astype(int)
        return self.vals[idx]


if __name__ == '__main__': 
    year = 2021
    noise = MyNoise(year)
    print(f"{year}: {noise.p}")
    print(f"{noise.noise((0,0))}")
