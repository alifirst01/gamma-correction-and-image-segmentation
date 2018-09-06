from collections import namedtuple
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import random
from matplotlib.colors import from_levels_and_colors
from collections import defaultdict

Pixel = namedtuple("Pixel", "m n")
image = cv2.imread(os.path.join('Data', 'img22gd2.tif'), 0)
height = len(image)
width = len(image[0])
segmentation_image = np.ones((height, width, 3)) * -1
colors = []

def connectedNieghbors(s, T, image, width, height):
    c = []
    if abs(int(image[s.m][s.n]) - int(image[s.m - 1][s.n])) <= T:
        c.append(Pixel(s.m - 1, s.n))
    if s.m + 1 < width and abs(int(image[s.m][s.n]) - int(image[s.m + 1][s.n])) <= T:
        c.append(Pixel(s.m + 1, s.n))
    if abs(int(image[s.m][s.n]) - int(image[s.m][s.n - 1])) <= T:
        c.append(Pixel(s.m, s.n - 1))
    if s.n + 1 < height and abs(int(image[s.m][s.n]) - int(image[s.m][s.n + 1])) <= T:
        c.append(Pixel(s.m, s.n + 1))
    return len(c), c


def connectedSet(s0, T, image, width, height, classLabel):
    global colors
    #Y = np.ones((width, height)) * 255
    global segmentation_image
    B = [s0]
    count = 0
    pixels = []
    while len(B) != 0:
        s = B[0]
        B.remove(s)
        pixels.append(s)
        segmentation_image[s.m][s.n] = classLabel
        count += 1
        m, c = connectedNieghbors(s, T, image, width, height)
        B.extend([c0 for c0 in c if all(segmentation_image[c0.m][c0.n] == [-1,-1,-1]) and c0 not in B])

    if count < 100:
        for px in pixels:
            segmentation_image[px.m][px.n] = [0,0,0]
        colors.remove(classLabel)
    return count


def getColor():
    global colors
    while(1):
        r1 = random.randint(0, 255)
        r2 = random.randint(0, 255)
        r3 = random.randint(0, 255)
        if [r1,r2,r3] not in colors:
            colors.append([r1,r2,r3])
            break
    return [r1,r2,r3]

def main():
    global segmentation_image
    s = Pixel(m=67, n=45)
    T = 2
    # m, s_cset = connectedSet(s, T, image, len(image), len(image[0]), 0)
    # cv2.imwrite('s-connected.png', s_cset)
    #cv2.waitKey(0)
    no_of_seg = 0
    for i in range(height):
        for j in range(width):
            if all(segmentation_image[i][j] == [-1, -1, -1]):
                px = Pixel(m=i,n=j)
                m = connectedSet(px, T, image, len(image), len(image[0]), getColor())
                if m > 100:
                    no_of_seg += 1
    print('No of Segments:', no_of_seg)
    cv2.imwrite('test-connected.png', segmentation_image)

    #cv2.waitKey(0)

if __name__ == '__main__':
    exit(main())