import cv2  # install opencv from conda
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
# import numpy as np


class TestClass():
    def __init__(self, name):  # read the image
        self.fname = name
        self.img = mpimg.imread(self.fname)
        self.point = ()

    def getCoord(self):
        fig = plt.figure()
        #ax = fig.add_subplot(111)
        plt.imshow(self.img)

        # connect the action 'button_press' with the func 'onclie'
        cid = fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        plt.show()
        return self.point

    def __onclick__(self, click):
        # record the coordinates with the click
        self.point = (click.xdata, click.ydata)

        print('you pressed the point with x coordinates {:.1f} \
            and y coordinates {:.1f}'.format(click.xdata, click.ydata))
        return self.point

# folder such as Hc_1.0m_
folder = input("Please specify the image folder: ")

# create an empty dictionary for recording the click history
data = {'file_name':[], 'coord_x':[], 'coord_y':[]}

# loop for going through figures; 
# loop continues with closing the window of the last figure
file_path = "{}/scaled".format(folder)

imgs = sorted(os.listdir(file_path), key=lambda x: int(x.split('.')[0].split('_')[-1]))




for img in imgs:

    t = TestClass("{}/scaled/{}".format(folder,img))
    coordinates = t.getCoord()
    if coordinates: 
        with open(folder + "/coordinates.txt", 'a') as f:
            f.write("{} {} {}\n".format(img, coordinates[0], coordinates[1]))
    
    

