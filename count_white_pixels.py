import numpy as np
import cv2


def count_difference_white(home, guest, old_home, old_guest):
    white_pixels_home = 0
    white_pixels_guest = 0

    gray_home = cv2.cvtColor(home, cv2.COLOR_BGR2GRAY)
    gray_guest = cv2.cvtColor(guest, cv2.COLOR_BGR2GRAY)

    # Counting the number of pixels with given value
    white_pixels_home += np.count_nonzero(gray_home > 190)
    white_pixels_guest += np.count_nonzero(gray_guest > 190)
    difference = white_pixels_home - white_pixels_guest

    if (difference < -10 or difference > 10):
        gray_home_old = cv2.cvtColor(old_home, cv2.COLOR_BGR2GRAY)
        gray_guest_old = cv2.cvtColor(old_guest, cv2.COLOR_BGR2GRAY)
        white_pixels_home_old = np.count_nonzero(gray_home_old > 190)
        white_pixels_guest_old = np.count_nonzero(gray_guest_old > 190)
        difference_h = white_pixels_home - white_pixels_home_old
        difference_g = white_pixels_guest - white_pixels_guest_old
        if (difference_h < -10 or difference_h > 10):
            return -1
        elif(difference_g < -10 or difference_g > 10):
            return 1

    return 0
