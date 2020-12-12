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

### ID:14511263 
### Name: Hasan Syed
### URL: https://github.com/SHS10/ARC 

# def solve_5bd6f4ac(x):
#     # get shape data in different categories
#     num_rows = x.shape[0]
#     num_cols = x.shape[1]
#     # perform integer division to get the right quarter of the array 
#     # regardless of dimensions for extensibility to different dimensions.
#     x = x[0:num_rows//3, 2*(num_cols//3):num_cols]
#     return x

def solve_1a07d186(x):
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
    # if the returned values is the same length as the number of columns than the grids are 
    # horizontal
    # x = solver(x)
    if horizontal:
        x = solver(x)
        return x
    else:
        x = x.transpose()
        x = solver(x)
        x = x.transpose()
        return x

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

