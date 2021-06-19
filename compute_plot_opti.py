import numpy as np
import math
import os
import pickle
import numpy as np
import glob
from matplotlib import pyplot as plt
import sys
import time
# no. of points in x-direction
Row = 750
# no. of points in y-direction
Col = 400
# space between points
dx = 2
csv = ".csv"



def may_mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


# read txt file containing the prefix of file
with open("list.txt") as f:
    mylist = f.read().splitlines()

for comptage, xx in enumerate(mylist):
    may_mkdir(xx)

    file = 'results/' + xx + 'trhist_DENSITY_.csv' # Read the density csv file
    Romax = -math.inf # Overall max
    
    with open(file, "r") as f:

        for line_num, lines in enumerate(f):
            fields = lines.split() # split by whitesapce
            print('new time: {}'.format(fields[0]))
            outname = '{}/{}{}'.format(xx, line_num,csv) 
            # Fill in values
            # from list to numpy
            input2 = np.reshape(np.array(list(map(float,fields))[1:]), (Col, Row), order='F')
            
            
            # Compute gradients
            input = np.zeros((Col, Row)) # initilization
            diff_x = np.diff(input2, axis = 1) / dx
            diff_y = np.diff(input2, axis = 0) / dx
            # initialization
            sumdiff_x = np.zeros((Col-1, Row-1))
            sumdiff_y = np.zeros((Col-1, Row-1))

            for i in range(Col-1): 
                sumdiff_x[i,:] = np.sum(diff_x[i:i+2, :], axis =0 ) 
            for i in range(Row-1):
                sumdiff_y[:,i] = np.sum(diff_y[:, i:i+2], axis =1 )
            delta = np.sqrt(np.square(sumdiff_x * 0.5) + np.square(sumdiff_y*0.5))
            input[:Col-1, :Row-1] = delta[:, :]
            
            np.savetxt(outname, input, delimiter=' ') # save input
    # Drawing pictures
    print("Drawing pictures")

    csv_files = glob.glob(xx + "/*.csv")
    # sort files accosring to csv file number
    csv_files =  sorted(csv_files, key= lambda f: int(f.split('/')[-1].split('.')[0]))

    # FInd the maximum

    for f in csv_files:
        cur_f = np.genfromtxt(f, delimiter = ' ')
        Romax = max(Romax , np.amax(cur_f))
    
    # Draw pictures

    out_folder = "./{}/scaled".format(xx)
    may_mkdir(out_folder)
    
    
    for idx, f in enumerate(csv_files):
        cur_f = np.genfromtxt(f, delimiter = ' ')
        f_s = -cur_f / Romax
        f_s = np.exp(20 * f_s)

        # draw
        pic_name = os.path.join(out_folder, "Scaled_T_{}.pickle".format(idx))
        fig, ax = plt.subplots()
        if not ax:
            ax = plt.gca()
        
        im = ax.imshow(f_s, cmap='gray',origin='lower')
        cbar = ax.figure.colorbar(im, ax=ax)
        ax.set_xlim(0.0, 800.0)
        ax.set_ylim(0.0, 450.0)
        pickle.dump(fig, open(pic_name, 'wb'))
        plt.close()


    # Delete files
    for f in csv_files:
        os.remove(f)
    

    print("Done!")

    