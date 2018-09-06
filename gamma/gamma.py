import cv2
import numpy as np
import os

def gammaCorrection(gamma):
    linear = cv2.imread(os.path.join('Data', 'linear.tif'), 0)
    height = len(linear)
    width = len(linear[0])
    gamma_image = np.zeros((height, width))
    gamma_corrected_image = np.zeros((height, width))

    inv_gamma = 1 / gamma
    for i in range(height):
        for j in range(width):
            gamma_image[i][j] = 255 * ((linear[i][j] / 255) ** gamma)
            gamma_corrected_image[i][j] = 255 * ((linear[i][j] / 255) ** inv_gamma)
    cv2.imwrite('gamma_correction.png', gamma_corrected_image)
    cv2.imwrite('gamma_image.png', gamma_image)

def gammaImage():
    height = 900
    width = 1600
    checkerboard = np.ones((height, width)) * 255
    k = 0
    for i in range(0, height, 2):
        for j in range(0, width, 4):
            checkerboard[i][j + k] = 0
            checkerboard[i + 1][j + k] = 0
            checkerboard[i][j + k + 1] = 0
            checkerboard[i + 1][j + k + 1] = 0
        if k == 0:
            k = 2
        else:
            k = 0

    cv2.imwrite('checkerboard.png', checkerboard)
    Ic = (255 + 0) / 2

    g = 130
    gamma = 1.13
    uniform_gray = np.ones((height, width)) * g
    cv2.imwrite('uniform_gray.png', uniform_gray)

    interlaced = np.array(checkerboard)
    for i in range(0, height, 32):
        for j in range(0, width):
            for k in range(16):
                if i + k >= height:
                    break
                interlaced[i + k][j] = g
    Ig = 255 * ((g / 255) ** gamma)
    cv2.imwrite('interlaced.png', interlaced)
    return gamma
    #g = 138
    #gamma = 1.13
    #Ic = Ig = 127.5

if __name__ == '__main__':
    gammaCorrection(gammaImage())