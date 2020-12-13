#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.


# Code and report by Name:Hasan Syed, Student ID: 14511263
# *********************************
# *********************************
### Student ID:14511263 
# *********************************
# *********************************

### Name: Hasan Syed
# *********************************
# *********************************

### LINK TO GITHUB: https://github.com/SHS10/ARC 
# *********************************
# *********************************
### BETTER formatting availalbe in report in README.md format - check link.
### Check README.md for a better formatted version of the report.
### Check github for a notebook file for problem 6b9890af.
# **********************************
### Reflections:
###  For all the problems that I have solved and attempted to solve. The commonality that I have found between all of the problems is that there is need to find some 
###  kind of outlier or anomaly within the grid space. 
###  For all the implementations aside from the non trivial ones, there is a need to keep track of all of these anomalies and perform complex and often confusing index based 
###  manipulations. 
###  In terms of the work done by Chollet, both tasks 1a07d186 and 6b9890af share the charateristic of Object cohesion, where we have to consider non-zero entries as objects 
###  in the space. The lines in 1a07d186 and both the box and the anomaly and the scaling factor in 6b9890af. 
###  Other than that the problems are largely unique. Since what are are trying to achieve in each of these very different. 
###  **Libraries Used and Tooling**: In terms of the library and tooling and features of the Python language used, I have written all of this code using the numpy and python.
###  For finding the coordinates of anomlies the np.where and np.all and the np.any functions were sometimes useful. While Sometimes I have eshewed the use of numpy vectorization for the native 
###  python lists since it allowed me to follow the code flow more easily as it is often hard to visualise and understand what is happening in within loops. I have also used different numpy 
### functions such as transpose and array_split where it was useful to do so.  
# **********************************
def solve_5bd6f4ac(x):
    """
        - Problem : 5bd6f4ac \n
        *General Description* (Problem and solving it visually - intuition):
            I get the zoomed in grid, only containing the top right third of the original input grid.\n

        *Algorithm* (to  guide understandiing of the code)
            - First I get the dimensions of the input in width and height
            - Then I get the top 1/3 of rows from the input and the the last 2/3 of the columns
            - Reassign to x and return

    **status**: *fully solved* - all training examples and test case.
    """
    # get shape data in different categories
    num_rows = x.shape[0]
    num_cols = x.shape[1]
    # perform integer division to get the right quarter of the array 
    # regardless of dimensions for extensibility to different dimensions.
    x = x[0:num_rows//3, 2*(num_cols//3):num_cols]
    return x

def solve_1a07d186(x):
    """
    - Problem : 1a07d186
    * General Description (Problem and solving it visually - intuition):
        - I want detect the individual grids to either side of the matching colored vertical or horizontal lines whichever is nearest. Otherwise I can delete them. I then translate individual colors to the the nerarest side of the appropriate color matching line.\n 
    
    * Algorithm (to guide understanding of the code)
     - Find where the there are non-empty grids.
     - Convert to transpose (for ease of programming), only if the lines vertical - this helps simplify the below computation. 
     - Find the coordinates of the lines.
     - From the non-empty grids that are not on the rows check if any of them match the colors of the lines. Note positions.
     - Check which row the individual matching color occurs. 
     - If the line are rows infront of the matching invididual, translate the row value to the line-row-index-1, attach above/beside the line. The column does not need to changed as I only handle all cases as vertical. If the matching line is rows behind the original value translate the row index of the individual point to the lines row index - 1. And keep the column index the same.
     - Convert back the transpose back to the original shape and return as x.

    **status**: *fully solved* - all training examples and the test case. 

    """
#   step 1: find horizontal or verticle lines that contain none black continous lines.
    # If the lines are horizontal, the followuing will return index of rows in x 

    contains_horizontal_boole_arr = [np.all(elems != 0) for elems in x]
    horizontal = False
    if any(contains_hz_boole == True for contains_hz_boole in contains_horizontal_boole_arr):
        horizontal = True
    
    def solver(x):
        cp_x = x.copy()
        def get_non_zero_cords(x): 
        # get the coords for non-zero values
            non_z = np.where(x != 0)
            row = non_z[0]
            col = non_z[1]
            nz_cords = np.dstack((row,col))
            # remove extra unused dimension from the array
            nz_cords = nz_cords[0, :, :]
            return nz_cords

        nz_cords = get_non_zero_cords(x)
        
        # detect the lines  
        line_vals = list()
        line_idx_row = list()
        for index, elems in enumerate(x):
            if np.all(elems != 0):
                line_vals.append(elems)
                line_idx_row.append(index)
        
        # use both nz_cords with along the detected lines to find the unique 
        # squares that need to be accounted for
        
        line_val_single = [elems[0] for elems in line_vals]
        
        # replace grids with non-continous line values with black.
        for cords in nz_cords:
            if np.any(cp_x[cords[0],cords[1]] not in line_val_single):
                cp_x[cords[0],cords[1]] = 0
        
        # refresh the non-zero cords since update above.
        nz_cords = get_non_zero_cords(cp_x)
        
        outliers_idx = list()   
        for cords in nz_cords:
            if cords[0] not in line_idx_row:
                    outliers_idx.append(cords)
            
        outliers_idx = np.array(outliers_idx)

        for index, elems in enumerate(outliers_idx):
        # get the ouliers vals - the colors themselves    
        # compare to against values 
            if cp_x[elems[0],elems[1]] in line_val_single:
                outlier_val = cp_x[elems[0],elems[1]]
                for idx in line_idx_row:
                    val_at_line = cp_x[idx][0]
                    if outlier_val == val_at_line:
                        outlier_row = elems[0]
                        if outlier_row < idx:
                            cp_x[elems[0],elems[1]] = 0
                            cp_x[idx-1, elems[1]] = outlier_val
                        if outlier_row > idx:
                            cp_x[elems[0],elems[1]] = 0
                            cp_x[idx+1, elems[1]] = outlier_val
            
        return cp_x

    # find if there are values occurring repeatedly in the vertical
    if horizontal:
        return solver(x)
    else:
        # convert to a horizontal format
        x = x.transpose()
        return solver(x).transpose()

def solve_6b9890af(x):
    """
    - Problem : **6b9890af**\n 
    - General Description: I want to place the anomaly into the red box, and scale the anomaly relative to the red box and return this.\n
    - Algorithm (to guide understanding of the code)\n
        - Find the box from the space - I assume that it is always square and is always red (2): so getting the first row is enough.
        - Create the red square
        - Get the coordinates of the anomaly in the original product. Note the coordinates. 
        - Find the minimum value that occurs in the rows and cols respectively from the anomaly coordinates. 
        - Convert them to a range between 0-3 by getting the modulus of the indexes with minimum index value. (assumption here is that I will always be working with anomalies of dimension 3x3)/
        - The scaling is calculated for the box by dividing the internal dimension of the box by 3. And the returning value is a added when specifying where to end a row and column. If division returns 1 i.e. the theres no upscaling. I set scaling to be 0. 
        - Split the internal area of the red block into thirds. 
        - For the row coordinates of the 0-3 encoded anamoly array I find the matching third of the split box. 
        - These are starting coordinates (apart from the starting point for rows which can be gotten from the intersection of the internal area). 
        - Fill the internal area of the box with the value of the anomaly.  

    **status**: *partially solved  - Test case and training example 3 fully passing. \nUnknown error for the example 2. \nAnd unusual behavior for example 1.
    \nAs a similar example has been tested in and showed to work in the notebook. 
    \nPlease check github for link to the github where the notebook NB_6b9890af.ipynb can be found in src to illustrate an example similar to example 1**
    """

    box_cords = list()
    # get the first horizontal line of the red box
    # don't need all of the coords for the scaling
    for index, elems in enumerate(x):
        if np.any(elems == 2):
            box_cords.append(index)


    # get the cords for the anomaly that I want to place in the box    
    anom_cords = np.where((x != 0) & (x!=2))
    min_val_row = np.amin(anom_cords[0])
    min_val_col = np.amin(anom_cords[1]) 
    
    # I need to encode the box coords into the the range from 0-3
    encd_rows = np.mod(anom_cords[0], min_val_row)
    encd_cols = np.mod(anom_cords[1], min_val_col)
    encd_cords = list(zip(encd_rows,encd_cols))
    encd_cords = np.array(encd_cords)

    # get the anomaly val
    anom_cords = list(zip(*anom_cords))
    anom_vals = [x[cords] for cords in anom_cords][0]
    
    box_xy = len(box_cords)
    new_x = np.zeros((box_xy,box_xy))
    new_x[:,0] = 2
    new_x[0] = 2
    new_x[box_xy-1]=2
    new_x[:,box_xy-1]=2

    
    # scaling aditive - creating scaling aditive that is used to 
    # amplify the anamoly in the postions - this is the factor of 
    # the internal length of empty space in the box.
    # if there is no scaling to be done, set the scaling to 0    
    scaling_aditive = int((box_xy-2)/3)
    if scaling_aditive <= 1:
        scaling_aditive = 0
        
    # split the area into thirds excluding the red box of 2s
    internal_area = np.where(new_x == 0)
    internal_area = list(zip(*internal_area))
    internal_area = np.array(internal_area)

    # dividing the area into thirds
    # Since I want to encode the anomaly in some enlarge space
    # And the anamolies are in a 3x3 grid, this utility is useful     
    internal_area_split = np.array_split(internal_area, 3)

    # since I scale the coordinates of the anamoly to a range
    # I can compare the index for the row triplets to the 
    # scaled rows directly.    
    for index, cords, in enumerate(internal_area_split):
        for idx, crds in enumerate(encd_cords):
            if index == crds[0]:
                start_point_row = internal_area_split[index][0][0]
                end_point_row = start_point_row+scaling_aditive
                cols_start = (crds[1]*scaling_aditive)+1
                cols_end = cols_start+scaling_aditive
                new_x[start_point_row:end_point_row, cols_start:cols_end] = anom_vals
                    
    x = new_x.astype(int)
    return x


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

