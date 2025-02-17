import numpy as np
import cv2
import config

h = config.H

def mult(vectors):
    for i in range(len(vectors)):
        k = h / vectors[i][1]
        vectors[i] = k * vectors[i]
    return vectors
