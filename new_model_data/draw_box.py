import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector

# global constants
img = None
tl_list = []
br_list = []
object_list = []

# constants
image_folder = 'referee_images'
savedir = 'annotations'
obj = 'referee'

if __name__ == '__main__':
    for n, image_file in enumerate(os.scandir(image_folder)):
        img = image_file
        fig, ax = plt.subplots(1, figsize=(10.5, 8))
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)
        plt.show()