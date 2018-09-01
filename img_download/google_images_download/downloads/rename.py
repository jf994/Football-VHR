import os
import urllib.request as ulib
from bs4 import BeautifulSoup as Soup

def group_images(folder_name):
    imdir = str(folder_name)+"_images"

    folders = [folder for folder in os.listdir('.') if 'py' not in folder]

    if not os.path.isdir(imdir):
        os.mkdir(imdir)

    n = 0
    for folder in folders:
        print(folder)
        for imfile in os.scandir(folder):
            os.rename(imfile.path, os.path.join(imdir, '{:06}.png'.format(n)))
            n += 1
        os.rmdir(folder)

if __name__ == '__main__':
    group_images('train')