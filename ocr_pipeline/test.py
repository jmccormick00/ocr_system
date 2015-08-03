__author__ = 'jr'

import subprocess

if __name__ == '__main__':

    enhance = "stretch"
    filtersize = 25
    offset = 20
    unrotate = ""
    saturation =  ""
    trim = ""
    padamt = ""

    # Build the commands

    # Local adaptive thresholding
    # lat widthxheight{+-}offset{%}
    lat = "{0}x{1}+{2}".format(filtersize, filtersize, offset)

    #subprocess.call(["convert", "test/receipt.jpg", "-contrast-stretch", '0', "-colorspace", "gray", "-lat", lat, "test/test.png"])
    subprocess.call(["convert", "test/crop.png", "-colorspace", "gray", "-type", "grayscale", "-contrast-stretch", '0', "-lat", lat, "test/test.png"])
