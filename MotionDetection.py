#!/usr/bin/python

import picamera
import picamera.array
import time

def takeMotionImage(width, height):
    with picamera.PiCamera() as camera:
        #time.sleep(1)
        camera.resolution = (width, height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            return stream.array

def detectMotion(data1, data2, threshold, sensitivity, width, height):
    diffCount = 0;
    for w in range(0, width):
        for h in range(0, height):
            # get the diff of the pixel. Conversion to int
            # is required to avoid unsigned short overflow.
            diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
            if diff > threshold:
                diffCount += 1
        if diffCount > sensitivity:
            break;
    if diffCount > sensitivity:
        return True
