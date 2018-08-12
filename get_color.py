import cv2
import numpy as np

def count_nonblack_np(img):
    """Return the number of pixels in img that are not black.
    img must be a Numpy array with colour values along the last axis.

    """
    return img.any(axis=-1).sum()
def detect_team(image, show=True):
    # define the list of boundaries
    boundaries = [
        ([17, 15, 100], [50, 56, 200]),  # red
        ([25, 146, 190], [96, 174, 250])  # yellow
    ]
    i = 0
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)
        tot_pix = count_nonblack_np(image)
        color_pix = count_nonblack_np(output)
        ratio = color_pix / tot_pix
        print("ratio is:", ratio)
        if ratio > 0.001 and i == 0:
            return 'red'
        elif ratio > 0.001 and i == 1:
            return 'yellow'

        i += 1

        if show == True:
            cv2.imshow("images", np.hstack([image, output]))
            #if cv2.waitKey(0) & 0xFF == ord('q'):
                #cv2.destroyAllWindows()
    return 'not_sure'