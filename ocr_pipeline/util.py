__author__ = 'jr'

import os

def get_filelist(path, ext):
    """
    Returns a list of files in the path with the extension, ext
    """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.' + ext)]

def imageMagick(input, output):
