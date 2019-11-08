import re
from argparse import ArgumentParser
import os
from osgeo import gdal

PROJECTION = re.compile(r'AUTHORITY\["([A-Z]+)","([0-9]+)"\]')
MASK = re.compile(r'(.*)mask(.*)')

POWERS_OF_TWO = [128, 256, 512, 1024, 2048]


def check_power(pwr_of_two: int) -> bool:
    x = False
    for power in POWERS_OF_TWO:
        if pwr_of_two == power:
            x = True
            break
    return x


def build_up(path: str, pwr_of_two=512) -> None:
    """ This function takes a 64x64 input and allows the user to stitch
    the images into a larger one. The new size must be a power of 2
    larger than 64x64. """
    x = False
    # Make sure user inputs a power of 2 that is contained in POWERS_OF_TWO
    while(True):
        x = check_power(pwr_of_two)
        if x is False:
            print("\nIncorrect input.")
            print("Possible inputs: 128, 256, 512, 1024, 2048")
            print("try again: ", end="")
            try:
                pwr_of_two = int(input())
            except ValueError:
                pass
            continue
        else:
            break

    # THE PLAN AT THE MOMENT IS TO SORT THEM IN ORDER AND HOPEFULLY
    # THEY WILL BE IN THE CORRECT ORDER

    REGEX = re.compile(r"(.*)_b([0-9]+).tif")
    for root, dirs, files in os.walk(path):
        for file in files:
            m = re.match(REGEX, file)
            if not m or not file.endswith('.tif'):
                continue
            _, num = m.groups()
            num = int(num)

            try:
                tif = gdal.Open(os.path.join(root, file))
            except AttributeError:
                continue

            # Check to make sure the image isn't a full granule
            if tif.RasterXSize > 2048:
                print(file)
                continue


if __name__ == "__main__":
    # TODO: Remove after done with testing
    p = ArgumentParser()
    p.add_argument("path", help='path to the folder with imgs')
    # p.add_argument("power", help='Enter a power of two')

    args = p.parse_args()
    build_up(args.path)